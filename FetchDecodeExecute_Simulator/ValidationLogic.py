
class Validate:
    @staticmethod
    def validate(ram_entries):
        if not ram_entries:
            return False

        for entry in ram_entries:
            if not Validate.is_valid_entry(entry):
                return False
        return True

    @staticmethod
    def is_valid_entry(entry):
        valid_instructions = {"load", "add", "sub", "mul", "div", "mod", "store", "jump", "for", "if"}

        instructions = entry.split()

        if len(instructions) == 0 or len(instructions) > 5:
            return False

        if len(instructions) == 1:
            if not instructions[0].isdigit():
                return False

        if len(instructions) == 2:
            if instructions[0] not in valid_instructions:
                return False
            if not instructions[1].isdigit() or not 0 <= int(instructions[1]) <= 7:
                return False

        if len(instructions) == 3:
            if instructions[0] not in valid_instructions:
                return False
            if not instructions[1].isdigit() or not 0 <= int(instructions[1]) <= 7:
                return False
            if not instructions[2].isdigit() or not 0 <= int(instructions[2]) <= 7:
                return False

        if len(instructions) == 5:
            valid_comparators = {">", ">=", "<", "<=", "==", "!="}
            if instructions[0] not in valid_instructions:
                return False
            if not instructions[1].isdigit() or not 0 <= int(instructions[1]) <= 7:
                return False
            if instructions[2] not in valid_comparators:
                return False
            if not instructions[3].isdigit() or not 0 <= int(instructions[3]) <= 7:
                return False
            if not instructions[4].isdigit() or not 0 <= int(instructions[4]) <= 7:
                return False

        return True
