"""
A pan-gram is a sentence where every letter of the English alphabet appears at least once.

Given a string sentence containing only lowercase English letters,
return true if sentence is a pangram, or false otherwise.

sentence = "thequickbrownfoxjumpsoverthelazydog"
True

sentence = "leetcode"
False

https://leetcode.com/problems/check-if-the-sentence-is-pangram/description/
"""


def checkIfPangram(sentence: str) -> bool:
    # return set(sentence) == set("abcdefghijklmnopqrstuvwxyz")

    return len(set(sentence)) == 26  # number of letters in the English alphabet


if __name__ == "__main__":
    sentence = "thequickbrownfoxjumpsoverthelazydog"
    # sentence = "coachable"
    print(checkIfPangram(sentence))
