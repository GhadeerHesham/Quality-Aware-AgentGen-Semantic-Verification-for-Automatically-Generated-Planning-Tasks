def extract_environment_text(sample):

        conversations = sample["conversations"]

        first_message = conversations[0]["value"]

        return first_message