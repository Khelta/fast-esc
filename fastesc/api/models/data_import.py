from datetime import datetime

from pydantic import BaseModel, Field, field_serializer, field_validator


class DataImportContest(BaseModel):
    year: int
    country: str
    city: str
    location: str
    broadcaster: str
    final: int
    date: str
    hosts: list[str] | None = None

    @field_validator("date")
    def validate_date(cls, date: str):
        try:
            datetime.strptime(date, "%d.%m.%Y").date()
        except ValueError:
            raise ValueError("Date must be in the format DD.MM.YYYY")
        return date

    @field_serializer("date")
    def serialize_date(self, date: str):
        return datetime.strptime(date, "%d.%m.%Y").date()


class DataImportParticipation(BaseModel):
    country: str = Field(examples=["ch"])
    artist: str = Field(examples=["Lys Assia"])
    title: str = Field(examples=["Refrain"])
    text: str | None = Field(default=None,
                             examples=[
                                 "(Refrain d'amour…)\n\nRefrain, couleur du ciel, parfum de mes vingt ans\nJardin plein de soleil où je courais enfant\nPartout je t'ai cherché, mon amoureux lointain\nGuettant par les sentiers où tu prenais ma main\n\nLes jours s'en sont allés et nous avons grandi\nL'amour nous a blessés, le temps nous a guéris\nMais seule et sans printemps\nJe cours en vain les bois, les champs\nDis, souviens-toi nos amours d'autrefois?\n\nLes années passent à tire-d'aile\nEt sur les toits de mon ennui coule la pluie\nOù sont parties les caravelles, volant mon cœur\nPortant mes rêves vers ton oubli?\nJ'aurais voulu que tu reviennes comme jadis\nPorter des fleurs à ma persienne\nEt ta jeunesse en mon logis\n\nRefrain, couleur de pluie, regret de mes vingt ans\nChagrin, mélancolie de n'être plus enfant\nMais seule et loin de toi, par les chemins où tu n'es pas\nJe vais, pleurant mes amours de vingt аnѕ"])
    languages: list[str] | None = None
    place: int | None = None
    running: int | None = None
    points: int | None = None
    public_points: int | None = None
    jury_points: int | None = None
    people: dict[str, list[str]] | None = Field(
        default=None,
        description="Dict where the keys are the role and the value is a list of all people who have this role.",
        examples=[{"ARTIST": ["Lys Assia"], "COMPOSER": ["G\u00e9o Voumard"]}],
    )


class DataImportSong(BaseModel):
    year: int
    final: int = Field(
        description="Decodes if the contest is a final (0) or semi-final (1) or (2)",
        examples=[0, 1, 2],
    )
    participations: list[DataImportParticipation]
