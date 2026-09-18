import random


def main() -> None:
	target = random.randint(1, 25)
	attempts = 0

	print("Guess the number from 1 to 25. You have 3 attempts.")

	while attempts < 3:
		try:
			guess = int(input("Enter your guess: "))
			if not 1 <= guess <= 25:
				raise ValueError
		except ValueError:
			print("Please enter a whole number from 1 to 25.")
			continue

		attempts += 1
		if guess == target:
			print("Correct!")
			return

	print(f"Sorry, the number was {target}.")


if __name__ == "__main__":
	main()
