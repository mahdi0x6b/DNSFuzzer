import argparse, os, interface_dns


# argparse config
parser = argparse.ArgumentParser()

input = parser.add_argument_group("input")
input.add_argument("-D","--domain", action="store", help="Domains to find subdomains for", required=True)
input.add_argument("-W","--wordlist", action="store", help="File containing words to bruteforce for domain", required=True)
input.add_argument("-S","--subdomains", action="store", help="File containing list of subdomains", required=True)
input.add_argument("-P","--permute", action="store", help="File containing list of permute word", required=True)
input.add_argument("-R","--resolver", action="store", help="File containing list of resolvers for enumeration", required=True)
input.add_argument("-M","--massdns", action="store", help="Path to the massdns binary")
input.add_argument("-Si","--silent", action="store_true", help="Disable logging")

output = parser.add_argument_group("output")
output.add_argument("-O", "--output", action="store", help="File to write output to")

args = parser.parse_args()

# interface config 
logger = interface_dns.Interface(args.silent)
logger.Banner()

# methods
def DnsGen(Flag, Subdomains, Output, Permute=None):
    if Flag == 1:
        # dnsgen passive output and permute(wordlist)
        command = "cat %s | dnsgen --wordlist %s - | tee %s > /dev/null 2>&1"%(Subdomains, Permute, Output)

    elif Flag == 2:
        # dnsgen subdomains with itself
        command = "echo '5254' > wordNull && cat %s | dnsgen --wordlist wordNull - | tee %s > /dev/null 2>&1"%(Subdomains, Output)
    
    returned_value = os.system(command)

def ShuffleDns(Subdomains, Resolver, Output, Massdns=None):
    if Massdns:
        command = "shuffledns -list %s -r %s -o %s -m %s -silent >> console.temp 2>&1"%(Subdomains, Resolver, Output, Massdns)
    else:
        command = "shuffledns -list %s -r %s -o %s -silent >> console.temp 2>&1"%(Subdomains, Resolver, Output)
    
    returned_value = os.system(command)

def CheckRequirement():
    from shutil import which
    
    if not(which("dnsgen")):
        logger.error("Dnsgen not installed.")
        return False

    if not(which("shuffledns")):
        logger.error("shuffledns not installed.")
        return False
    
    if not(which("anew")):
        logger.error("Anew not installed.")
        return False
     
    return True

def GetLen(Filename):
    return int(os.popen('wc -l %s'%(Filename)).read().split(  )[0])

# runner
def main():
    Domain = args.domain
    SubDomains = args.subdomains
    WordList = args.wordlist
    PermuteList = args.permute
    Resolver = args.resolver
    Output = args.output

    if not(CheckRequirement()):
        return 0

    TempOutputPhase1 = "OutputPhase1.temp" # dnsgen passiveSub and permute
    logger.info('Run Dnsgen on passive Subdoamins and permute list (out: %s)'%(TempOutputPhase1))
    DnsGen(1, SubDomains, TempOutputPhase1 ,PermuteList)
    
    logger.info('Removing out of scope subdomain from Dnsgen output')
    command = "sed -i '/%s$/!d' %s"%(Domain.replace(".","\."), TempOutputPhase1)
    returned_value = os.system(command)
    logger.info('Dnsgen generate %s in scope subdomain'%(GetLen(TempOutputPhase1)))


    OutputWordList = "OutputWordList.temp" # add domain end line wordlist
    logger.info('Make new subs from wordlist (out: %s)'%(OutputWordList))
    command = "sed s/$/%s/ %s > %s > /dev/null 2>&1"%("."+Domain.replace(".","\."), WordList, OutputWordList)
    returned_value = os.system(command)


    logger.info('Marge Dnsgen output and Wordlist (out: %s)'%(TempOutputPhase1))
    # marge wordlist and dnsgen(phase 1) output with anew
    command = "cat %s | anew %s -q >> console.temp 2>&1"%(OutputWordList, TempOutputPhase1)
    print(command)
    returned_value = os.system(command)
    os.remove(OutputWordList)

    logger.info('Run ShuffleDns on Dnsgen and wordlist output (out: %s)'%(Output))
    if args.massdns:
        ShuffleDns(TempOutputPhase1, Resolver, Output, Massdns=args.massdns)
    else:
        ShuffleDns(TempOutputPhase1, Resolver, Output)

    logger.info('ShuffleDns resolve %s subdomains'%(GetLen(Output)))
    os.remove(TempOutputPhase1)


    TempOutputPhase2 = "OutputPhase2.temp" 
    logger.info('Run Dnsgen on ShuffleDns output (out: %s)'%(TempOutputPhase2))
    DnsGen(2, Output, TempOutputPhase2)
    command = "sed -i '/5254/d' %s > /dev/null 2>&1"%(TempOutputPhase2)
    returned_value = os.system(command)
    
    logger.info('Removing out of scope subdomain from Dnsgen output')
    command = "sed -i '/%s$/!d' %s"%(Domain.replace(".","\."), TempOutputPhase2)
    returned_value = os.system(command)
    logger.info('Dnsgen generate %s subdomain from resolved subdomains'%(GetLen(TempOutputPhase2)))


    TempOutputPhase3 = "OutputPhase3.temp"
    logger.info('Run ShuffleDns on new Dnsgen output (out: %s)'%(TempOutputPhase3))
    if args.massdns:
        ShuffleDns(TempOutputPhase2, Resolver, TempOutputPhase3, Massdns=args.massdns)
    else:
        ShuffleDns(TempOutputPhase2, Resolver, TempOutputPhase3)
  
    logger.info('ShuffleDns resolve %s new subdomains'%(GetLen(TempOutputPhase3)))
    os.remove(TempOutputPhase2)

    logger.info('Generate final output (out: %s)'%(Output))
    command = "cat %s | anew %s -q >> console.temp 2>&1"%(TempOutputPhase3, Output)
    print(command)
    returned_value = os.system(command)
    logger.info('DnsBrute find %s new subdomains.'%(GetLen(TempOutputPhase3)))
    os.remove(TempOutputPhase3)
    logger.info('Finished. Good luck!')


if __name__ == "__main__":
    main()
