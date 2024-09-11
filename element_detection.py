# Analyze element data received from Arduino
def analyze_element_data(element_id):
    if element_id > 118:
        print("New element detected! Taking a sample.")
        return "COLLECT_SAMPLE"
    else:
        print(f"Known element detected: {element_id}")
        return "CONTINUE"
