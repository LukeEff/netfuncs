import sys
import json
import functools


def ipv4_to_value(ipv4_addr):
    """
    Convert a dots-and-numbers IP address to a single numeric value.

    Example:

    There is only one return value, but it is shown here in 3 bases.

    ipv4_addr: "255.255.0.0"
    return:    0xffff0000 0b11111111111111110000000000000000 4294901760

    ipv4_addr: "1.2.3.4"
    return:    0x01020304 0b00000001000000100000001100000100 16909060
    """
    sections = ipv4_addr.split(".")
    result = 0
    num = 24
    for part in sections:
        result = (int(part) << num) | result
        num = num - 8
    return result

def value_to_ipv4(addr):
    """
    Convert a single 32-bit numeric value to a dots-and-numbers IP
    address.

    Example:

    There is only one input value, but it is shown here in 3 bases.

    addr:   0xffff0000 0b11111111111111110000000000000000 4294901760
    return: "255.255.0.0"

    addr:   0x01020304 0b00000001000000100000001100000100 16909060
    return: "1.2.3.4"
    """
    res = []
    and_me = 0x000000ff
    for i in range(0, 32, 8):
        res.insert(0, (addr >> i) & and_me)
    return functools.reduce(lambda a, b: str(a) + "." + str(b), res)

def set_bit(num, digit):
    return num | (1 << digit)

def set_bits(num, begin, end):
    for i in range(begin, end):
        num = set_bit(num, i)
    return num

def get_subnet_mask_value(slash):
    """
    Given a subnet mask in slash notation, return the value of the mask
    as a single number. The input can contain an IP address optionally,
    but that part should be discarded.

    Example:

    There is only one return value, but it is shown here in 3 bases.

    slash:  "/16"
    return: 0xffff0000 0b11111111 11111111 00000000 00000000 4294901760

    slash:  "10.20.30.40/23"
    return: 0xfffffe00 0b11111111111111111111111000000000 4294966784
    """
    begin = 32 - int(slash.split("/")[-1])
    end = 32
    return set_bits(0, begin, end)

def ips_same_subnet(ip1, ip2, slash):
    """
    Given two dots-and-numbers IP addresses and a subnet mask in slash
    notataion, return true if the two IP addresses are on the same
    subnet.

    FOR FULL CREDIT: this must use your get_subnet_mask_value() and
    ipv4_to_value() functions. Don't do it with pure string
    manipulation.

    This needs to work with any subnet from /1 to /31

    Example:

    ip1:    "10.23.121.17"
    ip2:    "10.23.121.225"
    slash:  "/23"
    return: True
    
    ip1:    "10.23.230.22"
    ip2:    "10.24.121.225"
    slash:  "/16"
    return: False
    """
    mask = get_subnet_mask_value(slash)
    ip1_value = ipv4_to_value(ip1)
    ip2_value = ipv4_to_value(ip2)
    return ip1_value & mask == ip2_value & mask

def get_network(ip_value, netmask):
    """
    Return the network portion of an address value.

    Example:

    ip_value: 0x01020304
    netmask:  0xffffff00
    return:   0x01020300
    """
    return ip_value & netmask

def find_router_for_ip(routers, ip):
    """
    Search a dictionary of routers (keyed by router IP) to find which
    router belongs to the same subnet as the given IP.

    Return None if no routers is on the same subnet as the given IP.

    FOR FULL CREDIT: you must do this by calling your ips_same_subnet()
    function.

    Example:

    [Note there will be more data in the routers dictionary than is
    shown here--it can be ignored for this function.]

    routers: {
        "1.2.3.1": {
            "netmask": "/24"
        },
        "1.2.4.1": {
            "netmask": "/24"
        }
    }
    ip: "1.2.3.5"
    return: "1.2.3.1"


    routers: {
        "1.2.3.1": {
            "netmask": "/24"
        },
        "1.2.4.1": {
            "netmask": "/24"
        }
    }
    ip: "1.2.5.6"
    return: None
    """
    for router_ip, router in routers.items():
        if ips_same_subnet(ip, router_ip, router["netmask"]):
            return router_ip

# Uncomment this code to have it run instead of the real main.
# Be sure to comment it back out before you submit!
"""
def my_tests():
    print("-------------------------------------")
    print("This is the result of my custom tests")
    print("-------------------------------------")

    # Tests for ipv4_to_value
    assert(ipv4_to_value("255.255.0.0") == 0xffff0000)
    print("ipv4_to_value({})  ".format("255.255.0.0"), "\033[92m" + "PASSED" + "\033[0m")
    assert(ipv4_to_value("1.2.3.4") == 0x01020304)
    print("ipv4_to_value({})  ".format("1.2.3.4"), "\033[92m" + "PASSED" + "\033[0m")

    # Tests for value_to_ipv4
    assert(value_to_ipv4(0xffff0000) == "255.255.0.0")
    print("value_to_ipv4({})  ".format(hex(0xffff0000)), "\033[92m" + "PASSED" + "\033[0m")
    assert(value_to_ipv4(0x01020304) == "1.2.3.4")
    print("value_to_ipv4({})  ".format(hex(0x01020304)), "\033[92m" + "PASSED" + "\033[0m")

    # Tests for get_subnet_mask_value
    assert(get_subnet_mask_value("/16") == 0xffff0000)
    print("get_subnet_mask_value({})  ".format("/16"), "\033[92m" + "PASSED" + "\033[0m")
    assert(get_subnet_mask_value("10.20.30.40/23") == 0xfffffe00)
    print("get_subnet_mask_value({})  ".format("10.20.30.40/23"), "\033[92m" + "PASSED" + "\033[0m")

    # Tests for ips_same_subnet
    assert(ips_same_subnet("10.23.121.17", "10.23.121.225", "/23"))
    print("ips_same_subnet({}, {}, {})  ".format("10.23.121.17", "10.23.121.225", "/23"), "\033[92m" + "PASSED" + "\033[0m")
    assert(not ips_same_subnet("10.23.230.22", "10.24.121.225", "/16"))
    print("ips_same_subnet({}, {}, {})  ".format("10.23.230.22", "10.24.121.225", "/16"), "\033[92m" + "PASSED" + "\033[0m")

    # Tests for get_network
    assert(get_network(0x01020304, 0xffffff00) == 0x01020300)
    print("get_network({}, {})  ".format(hex(0x01020304), hex(0xffffff00)), "\033[92m" + "PASSED" + "\033[0m")

    # Tests for find_router_for_ip
    routers = {
        "1.2.3.1": {
            "netmask": "/24"
        },
        "1.2.4.1": {
            "netmask": "/24"
        }
    }
    assert(find_router_for_ip(routers, "1.2.3.5") == "1.2.3.1")
    print("find_router_for_ip({}, {})  ".format(routers, "1.2.3.5"), "\033[92m" + "PASSED" + "\033[0m")

    routers = {
        "1.2.3.1": {
            "netmask": "/24"
        },
        "1.2.4.1": {
            "netmask": "/24"
        }
    }
    assert(find_router_for_ip(routers, "1.2.5.6") is None)
    print("find_router_for_ip({}, {})  ".format(routers, "1.2.5.6"), "\033[92m" + "PASSED" + "\033[0m")

    print("-------------------------------------")
    print("End of my custom tests")
    print("-------------------------------------")
"""
## -------------------------------------------
## Do not modify below this line
##
## But do read it so you know what it's doing!
## -------------------------------------------

def usage():
    print("usage: netfuncs.py infile.json", file=sys.stderr)

def read_routers(file_name):
    with open(file_name) as fp:
        json_data = fp.read()
        
    return json.loads(json_data)

def print_routers(routers):
    print("Routers:")

    routers_list = sorted(routers.keys())

    for router_ip in routers_list:

        # Get the netmask
        slash_mask = routers[router_ip]["netmask"]
        netmask_value = get_subnet_mask_value(slash_mask)
        netmask = value_to_ipv4(netmask_value)

        # Get the network number
        router_ip_value = ipv4_to_value(router_ip)
        network_value = get_network(router_ip_value, netmask_value)
        network_ip = value_to_ipv4(network_value)

        print(f" {router_ip:>15s}: netmask {netmask}: " \
            f"network {network_ip}")

def print_same_subnets(src_dest_pairs):
    print("IP Pairs:")

    src_dest_pairs_list = sorted(src_dest_pairs)

    for src_ip, dest_ip in src_dest_pairs_list:
        print(f" {src_ip:>15s} {dest_ip:>15s}: ", end="")

        if ips_same_subnet(src_ip, dest_ip, "/24"):
            print("same subnet")
        else:
            print("different subnets")

def print_ip_routers(routers, src_dest_pairs):
    print("Routers and corresponding IPs:")

    all_ips = sorted(set([i for pair in src_dest_pairs for i in pair]))

    router_host_map = {}

    for ip in all_ips:
        router = find_router_for_ip(routers, ip)
        
        if router not in router_host_map:
            router_host_map[router] = []

        router_host_map[router].append(ip)

    for router_ip in sorted(router_host_map.keys()):
        print(f" {router_ip:>15s}: {router_host_map[router_ip]}")

def main(argv):
    if "my_tests" in globals() and callable(my_tests):
        my_tests()
        return 0

    try:
        router_file_name = argv[1]
    except:
        usage()
        return 1

    json_data = read_routers(router_file_name)

    routers = json_data["routers"]
    src_dest_pairs = json_data["src-dest"]

    print_routers(routers)
    print()
    print_same_subnets(src_dest_pairs)
    print()
    print_ip_routers(routers, src_dest_pairs)

if __name__ == "__main__":
    sys.exit(main(sys.argv))
    
