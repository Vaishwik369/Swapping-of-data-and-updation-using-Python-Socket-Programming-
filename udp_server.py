import socket

# Routing table for R2
routing_table = {
    'R1': {'R1': {'distance': 9999, 'reg_number': '', 'name': ''}, 
    'R2': {'distance': 9999, 'reg_number': '', 'name': ''}},
    'R2': {'R1': {'distance': 1, 'reg_number': '', 'name': ''}, 
    'R2': {'distance': 0, 'reg_number': '21BIT0003', 'name': 'Vaishwik'}}
}


def receive_routing_table():
    server_address = ('localhost', 12345)  # Change the address if necessary
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    server_socket.bind(server_address)

    print("Waiting for routing table from R1...")

    # Receive the routing table from R1
    routing_table_bytes, client_address = server_socket.recvfrom(4096)
    received_routing_table = eval(routing_table_bytes.decode('utf-8'))

    # Print the received routing table
    print("Received routing table at R2:")
    print_routing_table(received_routing_table)

    # Update the routing table at R2
    update_routing_table(received_routing_table)

    # Crash the link between R2 and R3
    crash_link('R2', 'R3')

    # Print the updated routing table
    print("\nUpdated routing table at R2:")
    print_routing_table(routing_table)

    # Send the updated routing table to R1
    updated_routing_table_bytes = str(routing_table).encode('utf-8')
    server_socket.sendto(updated_routing_table_bytes, client_address)
    print("Sent updated routing table to R1")

    server_socket.close()


def update_routing_table(received_routing_table):
    # Update the routing table at R2 based on the received routing table
    for source, distances in received_routing_table.items():
        for destination, info in distances.items():
            if destination not in routing_table:
                routing_table[destination] = {}
            if destination != 'R2':
                routing_table[destination][source] = {
                    'distance': info['distance'] + 1, 'reg_number': info['reg_number'], 'name': info['name']}


def crash_link(router1, router2):
    # Simulate a link crash between router1 and router2
    if router1 in routing_table and router2 in routing_table[router1]:
        routing_table[router1][router2]['distance'] = float('inf')
        routing_table[router2][router1]['distance'] = float('inf')


def print_routing_table(table):
    for source, distances in table.items():
        print(f"Source: {source}")
        for destination, info in distances.items():
            print(
                f"Destination: {destination}\tDistance: {info['distance']}\tReg Number: {info['reg_number']}\tName: {info['name']}")


if __name__ == '__main__':
    receive_routing_table()
