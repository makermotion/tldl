"""This file contains the prompt templates for the LLM."""

template = """
              Write a summary of the following text delimited by triple backticks.
              Return your response which covers all the key points of the text. make a middle detailed summary not too short or too long. Make the summary in {language} language.
              This summary will be synthesized into a speech, keep this in mid while writing the summary.
              ```{transcript}```
              SUMMARY:
           """
