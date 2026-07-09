from __future__ import annotations

from dataclasses import dataclass
import json
from pathlib import Path
from typing import Any


@dataclass(frozen=True)
class SectionItem:
    id: str
    question: str
    answer: str


@dataclass(frozen=True)
class Section:
    id: str
    title: str
    items: list[SectionItem]


@dataclass(frozen=True)
class Specialty:
    id: str
    code: str
    title: str
    study_period: str
    study_form: str
    places: str
    budget: str
    entrance_exam: str
    details: str


@dataclass(frozen=True)
class UsefulLink:
    id: str
    title: str
    url: str


class ContentRepository:
    def __init__(self, data_dir: str) -> None:
        self.data_dir = Path(data_dir)
        knowledge = self._read_json("knowledge_base.json")
        specialties = self._read_json("specialties.json")
        links = self._read_json("links.json")

        self.sections = self._load_sections(knowledge)
        self.specialties = self._load_specialties(specialties)
        self.links = self._load_links(links)

    def get_section(self, section_id: str) -> Section | None:
        return self.sections.get(section_id)

    def get_item(self, section_id: str, item_id: str) -> SectionItem | None:
        section = self.get_section(section_id)
        if section is None:
            return None
        return next((item for item in section.items if item.id == item_id), None)

    def get_specialty(self, specialty_id: str) -> Specialty | None:
        return self.specialties.get(specialty_id)

    def _read_json(self, filename: str) -> Any:
        path = self.data_dir / filename
        with path.open("r", encoding="utf-8") as file:
            return json.load(file)

    def _load_sections(self, data: dict[str, Any]) -> dict[str, Section]:
        sections: dict[str, Section] = {}
        for section in data["sections"]:
            items = [
                SectionItem(
                    id=item["id"],
                    question=item["question"],
                    answer=item["answer"],
                )
                for item in section.get("items", [])
            ]
            sections[section["id"]] = Section(
                id=section["id"],
                title=section["title"],
                items=items,
            )
        return sections

    def _load_specialties(self, data: dict[str, Any]) -> dict[str, Specialty]:
        specialties: dict[str, Specialty] = {}
        for item in data["specialties"]:
            specialties[item["id"]] = Specialty(
                id=item["id"],
                code=item["code"],
                title=item["title"],
                study_period=item["study_period"],
                study_form=item["study_form"],
                places=item["places"],
                budget=item["budget"],
                entrance_exam=item["entrance_exam"],
                details=item["details"],
            )
        return specialties

    def _load_links(self, data: dict[str, Any]) -> list[UsefulLink]:
        return [
            UsefulLink(id=item["id"], title=item["title"], url=item["url"])
            for item in data["links"]
        ]
