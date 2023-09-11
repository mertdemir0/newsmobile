from transformers import BartForConditionalGeneration, BartTokenizer

class TextSummarizer:
    """ 
    This class provides functionality to summarize text using the BART model.
    """
    def __init__(self, model_name="facebook/bart-large-cnn"):
        """
        Initializes the BART model and tokenizer.
        
        Args:
            model_name (str): The name of the pre-trained BART model. Defaults to "facebook/bart-large-cnn".
        """
        self.model = BartForConditionalGeneration.from_pretrained(model_name)
        self.tokenizer = BartTokenizer.from_pretrained(model_name)

    def summarize(self, text, max_input_length=1024, max_output_length=150):
        """
        Summarizes the input text using the BART model.
        
        Args:
            text (str): The input text to be summarized.
            max_input_length (int): The maximum length of the input text. Defaults to 1024.
            max_output_length (int): The maximum length of the summarized text. Defaults to 150.
            
        Returns:
            str: The summarized text.
        """
        inputs = self.tokenizer.encode(
            "summarize: " + text, return_tensors="pt", max_length=max_input_length, truncation=True
        )
        summary_ids = self.model.generate(
            inputs, max_length=max_output_length, min_length=30, length_penalty=2.0, num_beams=4, early_stopping=True
        )
        return self.tokenizer.decode(summary_ids[0], skip_special_tokens=True)