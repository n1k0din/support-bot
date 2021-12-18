import argparse
import json
from typing import Iterable, Sequence

from environs import Env
from google.cloud import dialogflow
from google.cloud.dialogflow_v2 import Intent


def get_questions(filename: str) -> dict:
    """Read questions from file."""
    with open(filename, 'r') as f:
        return json.load(f)


def create_dialogflow_intent(
    project_id: str,
    display_name: str,
    training_phrases_parts: Iterable[str],
    message_texts: Sequence[str],
) -> Intent:
    """Create an intent of the given intent type."""
    intents_client = dialogflow.IntentsClient()

    parent = dialogflow.AgentsClient.agent_path(project_id)
    training_phrases = []
    for training_phrases_part in training_phrases_parts:
        part = dialogflow.Intent.TrainingPhrase.Part(text=training_phrases_part)
        training_phrase = dialogflow.Intent.TrainingPhrase(parts=[part])
        training_phrases.append(training_phrase)

    text = dialogflow.Intent.Message.Text(text=message_texts)
    message = dialogflow.Intent.Message(text=text)

    intent = dialogflow.Intent(
        display_name=display_name,
        training_phrases=training_phrases,
        messages=[message],
    )

    return intents_client.create_intent(
        request={'parent': parent, 'intent': intent},
    )


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument(
        '--questions',
        default='questions.json',
        help='Questions to train DialogFlow, questions.json default',
    )

    args = parser.parse_args()
    questions_filename = args.questions    

    env = Env()
    env.read_env()
    dialogflow_project_id = env('DIALOGFLOW_PROJECT_ID')

    questions = get_questions(questions_filename)

    for topic, topic_questions_and_answer in questions.items():
        topic_answer = topic_questions_and_answer['answer']
        topic_questions = topic_questions_and_answer['questions']

        dialog_flow_response = create_dialogflow_intent(
            project_id=dialogflow_project_id,
            display_name=topic,
            training_phrases_parts=topic_questions,
            message_texts=[topic_answer],
        )
