from google.cloud import dialogflow


def get_dialogflow_answer(
    project_id: str,
    session_id: str,
    text: str,
    language_code: str = 'ru-RU',
) -> tuple[bool, str]:
    """Returns the result of detect intent with text as input."""
    session_client = dialogflow.SessionsClient()
    session = session_client.session_path(project_id, session_id)
    text_input = dialogflow.TextInput(text=text, language_code=language_code)
    query_input = dialogflow.QueryInput(text=text_input)

    response = session_client.detect_intent(
        request={
            'session': session,
            'query_input': query_input,
        },
    )

    query_result = response.query_result
    return query_result.intent.is_fallback, query_result.fulfillment_text
