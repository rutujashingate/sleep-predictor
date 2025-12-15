def generate_suggestions(input_dict):
    suggestions = []

    if input_dict.get("sleep_efficiency") and input_dict["sleep_efficiency"] < 85:
        suggestions.append("Improve sleep efficiency by reducing awakenings.")

    if input_dict.get("stress_score") and input_dict["stress_score"] > 6:
        suggestions.append("Try meditation or stress reduction techniques.")

    if input_dict.get("screen_time_before_bed_min") and input_dict["screen_time_before_bed_min"] > 30:
        suggestions.append("Reduce screen time before bed.")

    if input_dict.get("bedtime_consistency_std_min") and input_dict["bedtime_consistency_std_min"] > 30:
        suggestions.append("Maintain a consistent bedtime.")

    if not suggestions:
        suggestions.append("Great job! Your sleep habits seem healthy.")

    return suggestions
