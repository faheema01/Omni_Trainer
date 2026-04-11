from pydantic_ai import Agent
from multimodal_moderation.types.model_choice import ModelChoice
from multimodal_moderation.types.moderation_result import TextModerationResult


# Instructions sent to the LLM on every call.
# The output section must stay in sync with the fields defined in TextModerationResult:
#   contains_pii, is_unfriendly, is_unprofessional, rationale.
MODERATION_INSTRUCTIONS = """
<context>
At ACME enterprise we strive for a friendly but professional interaction with our customers.
</context>

<role>
You are a customer service reviewer at ACME enterprise. You make sure that the customer
service interactions are friendly and professional.
</role>

<input>
You will receive a message from the customer representative towards the customer.
</input>

<instructions>
Detect if:
- the tone of the message is unfriendly
- the tone of the message is unprofessional
- the message contains any personally-identifiable information (PII)
</instructions>

<output>
Provide a detailed rationale for your choices.
</output>
"""


# The agent wraps the LLM call and enforces the TextModerationResult schema.
# pydantic-ai validates and parses the model's JSON output into a
# TextModerationResult instance automatically.
text_moderation_agent = Agent(
    instructions=MODERATION_INSTRUCTIONS,
    output_type=TextModerationResult,
)


async def moderate_text(model_choice: ModelChoice, text: str) -> TextModerationResult:
    # Run the agent with the supplied text as the user prompt.
    # We pass model and model_settings from model_choice so callers can
    # swap models (e.g. for evals) without changing this function.
    result = await text_moderation_agent.run(
        text,
        model=model_choice.model,
        model_settings=model_choice.model_settings,
    )

    # result.output is already a validated TextModerationResult instance —
    # pydantic-ai parsed and type-checked the LLM response for us.
    return result.output
