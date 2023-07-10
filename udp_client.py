import socket

# Routing table for R1
routing_table = {
    'R1': {'R1': {'distance': 0, 'reg_number': '21BIT0080', 'name': 'Stark'}, 
    'R2': {'distance': 1, 'reg_number': '', 'name': ''}},
    'R2': {'R1': {'distance': 9999, 'reg_number': '', 'name': ''}, 
    'R2': {'distance': 9999, 'reg_number': '', 'name': ''}}
}


def send_routing_table():
    server_address = ('localhost', 12345)  # Change the address if necessary
    client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    # Serialize the routing table
    routing_table_bytes = str(routing_table).encode('utf-8')

    # Send the routing table to R2
    client_socket.sendto(routing_table_bytes, server_address)
    print("Sent routing table to R2")

    # Receive the updated routing table from R2
    updated_routing_table_bytes, _ = client_socket.recvfrom(4096)
    updated_routing_table = eval(updated_routing_table_bytes.decode('utf-8'))

    # Print the updated routing table
    print("Updated routing table at R1:")
    print_routing_table(updated_routing_table)

    client_socket.close()


def print_routing_table(table):
    for source, distances in table.items():
        print(f"Source: {source}")
        for destination, info in distances.items():
            print(
                f"Destination: {destination}\tDistance: {info['distance']}\tReg Number: {info['reg_number']}\tName: {info['name']}")


if __name__ == '__main__':
    send_routing_table()
