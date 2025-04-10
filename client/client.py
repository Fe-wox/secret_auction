from random import random, choice

import requests
import time

SERVER_URL = "http://127.0.0.1:5000"  # Server-Adress


def get_bidder_name():
    """Fragt nach einem gültigen Bieternamen."""
    while True:
        name = input("Please insert your name: ").strip()
        if len(name) == 0:
            print(" Invalid input . Name cannot be empty or blank . ")
        elif len(name) > 10:
            print(" Invalid input . Name must be 10 characters or less . ")
        else:
            return name


def get_bid_amount():
    """Fragt nach einem Gebot."""
    while True:
        try:
            bid_amount = float(input("Please enter your bid: $ "))
            if bid_amount > 0:
                return bid_amount
            else:
                print("Das Gebot muss größer als 0 sein!")
        except ValueError:
            print("Ungültige Eingabe. Bitte eine Zahl eingeben.")


def place_bid(name):
    """Sends a bid to the server."""
    bid_amount = get_bid_amount()
    response = requests.post(f"{SERVER_URL}/bid", json={"name": name, "amount": bid_amount})
    print(response.json()["message"])
    return bid_amount


def finish_bidding(name):
    """Indicates that the bidder is done with bidding."""
    response = requests.post(f"{SERVER_URL}/finish", json={"name": name})
    if response.status_code == 200:
        print(response.json()["message"])
        return True
    else:
        print(f"Error: {response.status_code}, {response.json().get('error', 'Unknown error')}")
        return False


def main():
    print("Welcome to the Secret Auction!")
    name = get_bidder_name()
    highest_bid = 0

    while True:
        bid = place_bid(name)
        if bid > highest_bid:
            highest_bid = bid

        update_bid = input("\nWould you like to raise your bid? (y/n): ").strip().lower()

        if update_bid == "n":
            print(f"\nThank you for participating. Your final bid is {highest_bid} $.")
            if finish_bidding(name):
                break
            else:
                print("Failed to confirm your bidding status.")
        elif update_bid == "y":
            continue
        else:
            print("Invalid input. Please only enter 'y' or 'n'.")

    timeout = 60
    start_time = time.time()

    while True:
        response = requests.get(f"{SERVER_URL}/winner")
        data = response.json()

        if "error" in data:
            print("Waiting for all bidders to finish...")
            time.sleep(3)
            if time.time() - start_time > timeout:
                print("Timeout: Not all bidders have finished within the expected time.")
                break
        else:
            if data.get("tie"):
                print("\nAuction has ended with a tie!")
                print(f"Amount: {data['amount']} $")
                tied_bidders = data["bidders"]
                print(f"Tied bidders: {', '.join(tied_bidders)}")

                # Zufälligen Gewinner aus den Bietern im Gleichstand wählen
                winner = choice(tied_bidders)
                print(f"\nThe randomly selected winner is: {winner} with a bid of {data['amount']} $.")

            elif data.get("winner"):
                winner = data.get("winner")
                amount = data.get("amount")
                print(f"\nAuction has ended!")
                print(f"The winner is {winner} with a bid of {amount} $.")
            else:
                print("\nAuction has ended! No bids were placed.")
            break


if __name__ == "__main__":
    main()
