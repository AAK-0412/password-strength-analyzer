from zxcvbn import zxcvbn
import itertools

def analyze_password(password):
    result = zxcvbn(password)
    print("\n Password Analysis:")
    print("Score (0-4):", result['score'])
    print("Estimated Crack Time:", result['crack_times_display']['offline_fast_hashing_1e10_per_second'])
    print("Warnings:", result['feedback']['warning'])
    print("Suggestions:", ", ".join(result['feedback']['suggestions']) if result['feedback']['suggestions'] else "None")

def generate_custom_wordlist(inputs, filename="wordlist.txt"):
    leet_replacements = {
        'a': ['a', '@', '4'],
        'e': ['e', '3'],
        'i': ['i', '1', '!'],
        'o': ['o', '0'],
        's': ['s', '$', '5']
    }

    def leetify(word):
        patterns = [[c] if c not in leet_replacements else leet_replacements[c] for c in word.lower()]
        return [''.join(p) for p in itertools.product(*patterns)]

    wordlist = set()

    for base in inputs:
        leet_versions = leetify(base)
        for word in leet_versions:
            wordlist.add(word)
            wordlist.add(word + "123")
            wordlist.add(word + "2025")
            wordlist.add(word.capitalize())
            wordlist.add(word[::-1])  # reversed

    with open(filename, "w") as f:
        for word in sorted(wordlist):
            f.write(word + "\n")

    print(f"\n Wordlist generated with {len(wordlist)} entries and saved to '{filename}'.")

if __name__ == "__main__":
    print(" Password Strength Analyzer & Custom Wordlist Generator\n")
    
    pw = input("Enter a password to analyze: ")
    analyze_password(pw)

    print("\n Now, let's generate a custom wordlist.")
    user_inputs = input("Enter names/dates/pets/etc (comma-separated): ").split(",")
    user_inputs = [i.strip() for i in user_inputs if i.strip() != ""]

    generate_custom_wordlist(user_inputs)
