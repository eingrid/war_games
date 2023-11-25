class Reward():
    def calculate_total_reward() -> float:
        """Calculates how successful this simulation was """
        return NotImplementedError()

    def calculate_step_reward() -> float:
        """Calculate how succesful this step was"""
        return NotImplementedError()