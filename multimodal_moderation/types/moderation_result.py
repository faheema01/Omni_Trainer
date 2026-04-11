from pydantic import BaseModel, Field


class ModerationResult(BaseModel):
    """Base class for all moderation results.

    Every moderation agent returns a subclass of this model. The base class
    holds the fields that are common to all moderation types and provides the
    `is_flagged` convenience property so callers never need to inspect individual
    flag names manually.
    """

    rationale: str = Field(description="Explanation of what was harmful and why")

    @property
    def is_flagged(self) -> bool:
        """Return True if any boolean moderation flag on this result is True.

        Implementation note: we use model_dump() to iterate all field values
        at runtime, so this property works for every subclass without needing
        to hard-code field names here in the base class.
        """
        return any(
            value
            for value in self.model_dump().values()
            if isinstance(value, bool)
        )


class TextModerationResult(ModerationResult):
    """Moderation result for plain-text customer-service messages."""

    # Whether the message exposes any customer PII (names, phone numbers, etc.)
    contains_pii: bool = Field(description="Whether the message contains any personally-identifiable information (PII)")
    # Whether the agent used a tone that could upset or offend the customer
    is_unfriendly: bool = Field(description="Whether unfriendly tone or content was detected")
    # Whether the agent's language was inappropriate for a professional setting
    is_unprofessional: bool = Field(description="Whether unprofessional tone or content was detected")


class ImageModerationResult(ModerationResult):
    """Moderation result for images attached to customer-service interactions."""

    # Catches faces, license plates, addresses visible in photos, etc.
    contains_pii: bool = Field(
        description="Whether the image contains any person, part of a person, or personally-identifiable information (PII)"
    )
    is_disturbing: bool = Field(description="Whether the image is disturbing")
    is_low_quality: bool = Field(description="Whether the image is low quality")


class VideoModerationResult(ModerationResult):
    """Moderation result for video clips attached to customer-service interactions."""

    # Catches people or identifying details captured in the video frames
    contains_pii: bool = Field(
        description="Whether the video contains any person or personally-identifiable information (PII)"
    )
    is_disturbing: bool = Field(description="Whether the video is disturbing")
    is_low_quality: bool = Field(description="Whether the video is low quality")


class AudioModerationResult(ModerationResult):
    """Moderation result for audio recordings of customer-service calls.

    Extends the base result with a verbatim transcription field so downstream
    systems can log or display the spoken content without re-transcribing it.
    """

    # The verbatim spoken content — produced by the agent before moderation flags are set
    transcription: str = Field(description="The transcription of the audio")
    # Catches names, account numbers, addresses, or other PII spoken aloud
    contains_pii: bool = Field(
        description="Whether the audio contains any personally-identifiable information (PII) such as names, addresses, phone numbers"
    )
    is_unfriendly: bool = Field(description="Whether unfriendly tone or content was detected")
    is_unprofessional: bool = Field(description="Whether unprofessional tone or content was detected")
