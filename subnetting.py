# WIP?

import re

class CustomException(Exception):
  """Custom Exception"""
  
def isValidIp(ip:str)-> bool:
    valid_regex=re.compile(r"^((25[0-5]|(2[0-4]|1\d|[1-9]|)\d)\.?\b){4}$")
    return valid_regex.match(ip)!=None

def bitsNeededPerHosts(hosts=2):
	count=0
	while True:
		hosts_per_count=2**count-2
		if (hosts_per_count>=hosts):
			return (count,hosts_per_count)
		count+=1

def intToBinary(number:int):
	return str(bin(number)[2:])


def binaryToInt(binary:str):
	return int(binary,2)

def decimalIpToBinary(ip:str|list[int]):
  ip_array=ip
  if type(ip_array) is str:
    if not isValidIp(ip): raise CustomException("Invalid IP")
    ip_array=[int(part) for part in ip_array.split('.')]
  
  result:list[str]=[]
  for part in ip_array:
    binary=intToBinary(part)
    result.append(("0"*(8-len(binary)))+binary)
    # result+=("0"*(8-len(binary)))+binary
  return result

def binaryIpToDecimal(ip:str|list[str]):
  ip_array=ip
  if type(ip_array) is str:
    if len(ip)!=32: raise CustomException("Invalid IP")
    ip_array=[ip_array[i:i+8] for i in range(0,32,8)]
  if len(ip_array) !=4: raise CustomException("Invalid IP")
  return [binaryToInt(part) for part in ip_array]



def get_ip_range(ip,sm,hostBits):
	binaryIp=''.join(decimalIpToBinary(ip))

	last_ip_bits=intToBinary(binaryToInt(binaryIp)+binaryToInt("0"*(32-hostBits) + "1"*hostBits))
	
	broadcast=binaryIpToDecimal(last_ip_bits)
	first_ip=ip[:3]+[ip[3]+1]
	last_ip=broadcast[:3]+[broadcast[3]-1]
	print(f"\tSTART IP: {forgeIp(ip)} /{32-hostBits}")
	print(f"\t\tSUBNET MASK : {forgeIp(sm)}")
	print(f"\t\tBROADCAST: {forgeIp(broadcast)}")
	print(f"\t\tHOSTS RANGE: {forgeIp(first_ip)} ─ {forgeIp(last_ip)}")
	print(f"\t\t\tTOTAL HOSTS: {2**hostBits-2}")

	nextip=binaryIpToDecimal(intToBinary(binaryToInt(''.join(decimalIpToBinary(broadcast)))+1))
	return nextip


def forgeIp(ip_array: list[int|str]):
  return (".".join(str(i) for i in ip_array))
def splitIp(ip:str):
  if not isValidIp(ip): raise CustomException("Invalid IP")
  return [int(i) for i in ip.split('.')]




if __name__=="__main__":
  raw=input(f"INITIAL IP [e.g. 192.168.1.0] : ")
  # raw:str="192.168.1.0"
  splitted=raw.split("/")

  initial_ip=splitted[0].strip() 
  if (not isValidIp(initial_ip)):
    print('Invalid IP')
    exit(1)
  initial_ip=splitIp(initial_ip)
  

  hosts=[]
  totalSubnets=int(input("N of subnets: "))
  for i in range(totalSubnets):
      hosts.append(int(input(f"[{i+1}]Subnet, hosts: ")))

  next_ip=initial_ip
  hosts=sorted(hosts,reverse=True)

  for i,host in enumerate(hosts):
    try:
      host=int(host)
      print(f"{i+1}: {host} hosts:")
    except:
      print(f"{i+1}: Unknown hosts:")
      continue
    
    bitsNeeded=bitsNeededPerHosts(host)
    
    host_bits=bitsNeeded[0]
    net_bits=32-host_bits

    subnet_mask_bits=("1"*net_bits) + ("0"*host_bits)
    subnet_mask_decimal=binaryIpToDecimal(subnet_mask_bits)
    start_ip=[next_ip[i]&subnet_mask_decimal[i] for i in range(4)]

    next_ip=get_ip_range(start_ip,subnet_mask_decimal,host_bits)