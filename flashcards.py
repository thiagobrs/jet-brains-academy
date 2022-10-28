import os
import random
import io
import argparse


class FlashCards:
    """A flashcard application."""

    ACTIONS = ['add', 'remove', 'import', 'export', 'ask', 'exit', 'log', 'hardest card', 'reset stats']

    def __init__(self):
        """Read the args and initialize the object variables."""

        parser = argparse.ArgumentParser(description="This is a flashcard app.")
        parser.add_argument("--import_from", help="The name of the file to import cards from on the initialization.")
        parser.add_argument("--export_to", help="The name of the file to export the cards on the exit.")

        self.args = parser.parse_args()
        self.cards = dict()
        self.mistakes = dict()
        self.menu = ', '.join(self.ACTIONS)
        self.log = io.StringIO()

    def get_card_from_description(self, description: str):
        """Return card for any description.

        Keyword arguments:
        description -- Description to look for."""

        for key, value in self.cards.items():
            if description == value:
                return key

        return "Card doesn't exist.\n"

    def message_handler(self, in_out: str, output_text: str = '') -> str:
        """Print a message or ask for the user input and register the I/O text in the log object.

        Keyword arguments:
        in_out -- 'I' for input or 'O' for output
        output_text -- The output message to print/log"""

        if in_out == 'I':
            input_text = input()
            print(input_text, file=self.log)
            return input_text
        elif in_out == 'O':
            print(output_text)
            print(output_text, file=self.log)

    def add(self):
        """Add a card/definition pair to the lists."""

        self.message_handler('O', "The card:")
        card = self.message_handler('I')
        while card in self.cards.keys():  # self.cards:
            self.message_handler('O', f'The term "{card}" already exists. Try again:')
            card = self.message_handler('I')

        self.message_handler('O', "The definition of the card:")
        definition = self.message_handler('I')
        while definition in self.cards.values():
            self.message_handler('O', f'The definition "{definition}" already exists. Try again:')
            definition = self.message_handler('I')

        self.cards[card] = definition

        self.message_handler('O', f'The pair ("{card}":"{definition}") has been added.\n')

    def remove(self):
        """Remove a card/definition pair from the lists."""

        self.message_handler('O', "Which card?")
        card = self.message_handler('I')

        if card in self.cards.keys():
            self.cards.pop(card)
            self.message_handler('O', "The card has been removed.\n")
        else:
            self.message_handler('O', f"Can't remove \"{card}\": there is no such card.\n")

    def import_flashcards(self, import_from: str = ''):
        """Load a flashcard collection from a given file.

        Keyword arguments:
        import_from -- name of the file to import cards from informed as argument at initialization"""

        if not import_from:
            self.message_handler('O', "File name:")
            file_name = self.message_handler('I')
        else:
            file_name = import_from

        if os.path.exists(file_name):
            try:
                # Try to open the file
                with open(file_name, "r", encoding='utf-8') as file:
                    new_cards = eval(file.readline())
                    self.cards.update(new_cards)
                    self.message_handler('O', f"{len(new_cards)} cards have been loaded.\n")
            except OSError:
                # If an error occur, show a message
                self.message_handler('O', "An error occurred while reading the file.\n")
        else:
            self.message_handler('O', "File not found.\n")

    def export_flashcards(self, export_to: str = ''):
        """Save flashcard collection to a file.

        Keyword arguments:
        export_to -- name of the file to export the cards, informed as argument at initialization"""

        if not export_to:
            self.message_handler('O', "File name:")
            file_name = self.message_handler('I')
        else:
            file_name = self.args.export_to

        try:
            # Try to open the file
            with open(file_name, "w", encoding='utf-8') as file:
                file.write(str(self.cards))
                self.message_handler('O', f"{len(self.cards)} cards have been saved.\n")
        except OSError:
            # If an error occur, show a message
            self.message_handler('O', "An error occurred while writing the file.\n")

    def ask(self):
        """Prompt the user for cards definitions."""

        self.message_handler('O', "How many times to ask?")
        num_cards = int(self.message_handler('I'))

        for num in range(num_cards):
            # Choose a random card and ask the user for its definition
            card, definition = random.choice(list(self.cards.items()))
            self.message_handler('O', f'Print the definition of "{card}":')
            answer = self.message_handler('I')

            # Analyze the answer
            if answer == definition:
                self.message_handler('O', "Correct!")
            else:
                # Update the number of mistakes for this card
                self.mistakes[card] = self.mistakes.get(card, 0) + 1

                if answer in self.cards.values():
                    valid_card = self.get_card_from_description(answer)
                    self.message_handler('O', f'Wrong. The right answer is "{definition}", but your definition is correct for "{valid_card}".')
                else:
                    self.message_handler('O', f'Wrong. The right answer is "{definition}".')

        self.message_handler('O', "")

    def save_log(self):
        """Save the log messages to a file."""

        self.message_handler('O', 'File name:')
        file_name = self.message_handler('I')
        with open(file_name, mode='w') as f:
            print(self.log.getvalue(), file=f)
        self.message_handler('O', 'The log has been saved.\n')

    def hardest_card(self):
        """Print the term(s) with the highest number of wrong answers."""

        if len(self.mistakes) == 0:
            self.message_handler("O", "There are no cards with errors.\n")
        else:
            # Find the card with max number of mistakes
            max_mistakes = max(self.mistakes, key=self.mistakes.get)

            # Find other cards with the same number of mistakes than max_mistakes
            hardest_cards = [key for key, value in self.mistakes.items() if value == self.mistakes[max_mistakes]]

            if len(hardest_cards) == 1:
                self.message_handler('O', f'The hardest card is "{max_mistakes}". You have {self.mistakes[max_mistakes]} errors answering it.\n')
            else:
                hardest_cards_text = 'The hardest cards are "' + '", '.join(hardest_cards) + '".\n'
                self.message_handler('O', hardest_cards_text)

    def reset_stats(self):
        """Print the term or terms that the user makes most mistakes."""

        self.mistakes.clear()
        self.message_handler('O', "Card statistics have been reset.\n")

    def exit(self):
        """Terminate the program."""

        # Check if the export_to argument was informed at the initialization
        if self.args.export_to:
            self.export_flashcards(self.args.export_to)

        self.message_handler('O', "Bye bye!")
        self.log.close()

    def run(self):
        """Start the flashcard application."""

        # Check if the import_from argument was informed at the initialization
        if self.args.import_from:
            self.import_flashcards(self.args.import_from)

        # Show the menu until action == exit
        while True:
            self.message_handler('O', f"Input the action ({self.menu}):")
            action = self.message_handler('I')

            # Check if the action is valid
            if action in self.ACTIONS:
                if action == 'exit':
                    self.exit()
                    break
                elif action == 'add':
                    self.add()
                elif action == 'remove':
                    self.remove()
                elif action == 'import':
                    self.import_flashcards()
                elif action == 'export':
                    self.export_flashcards()
                elif action == 'ask':
                    self.ask()
                elif action == 'log':
                    self.save_log()
                elif action == 'hardest card':
                    self.hardest_card()
                elif action == 'reset stats':
                    self.reset_stats()
            elif action == 'print':  # Bonus hidden action, just to know the state of the cards and mistakes in memory
                print("Cards:")
                print(str(self.cards))
                print("Mistakes:")
                print(str(self.mistakes))
            else:
                self.message_handler('O', f'Invalid action: "{action}".')


def main():
    """Create a flashcard application and execute it."""

    flashcard = FlashCards()
    flashcard.run()


if __name__ == "__main__":
    main()
