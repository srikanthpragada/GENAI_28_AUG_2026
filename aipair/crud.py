"""CRUD operations for a SQLite ``courses`` table."""

from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable


@dataclass(frozen=True)
class Course:
	"""A course stored in the database."""

	id: int | None
	code: str
	name: str
	instructor: str
	credits: int


class CourseRepository:
	"""Create and manage courses in a SQLite database."""

	def __init__(self, database: str | Path = "courses.db") -> None:
		self.connection = sqlite3.connect(database)
		self.connection.row_factory = sqlite3.Row
		self.create_table()

	def create_table(self) -> None:
		"""Create the courses table when it does not already exist."""
		self.connection.execute(
			"""
			CREATE TABLE IF NOT EXISTS courses (
				id INTEGER PRIMARY KEY AUTOINCREMENT,
				code TEXT NOT NULL UNIQUE,
				name TEXT NOT NULL,
				instructor TEXT NOT NULL,
				credits INTEGER NOT NULL CHECK (credits > 0)
			)
			"""
		)
		self.connection.commit()

	@staticmethod
	def _to_course(row: sqlite3.Row) -> Course:
		return Course(
			id=row["id"],
			code=row["code"],
			name=row["name"],
			instructor=row["instructor"],
			credits=row["credits"],
		)

	def create(
		self, code: str, name: str, instructor: str, credits: int
	) -> Course:
		"""Insert a course and return the newly created record."""
		cursor = self.connection.execute(
			"""
			INSERT INTO courses (code, name, instructor, credits)
			VALUES (?, ?, ?, ?)
			""",
			(code, name, instructor, credits),
		)
		self.connection.commit()
		return self.get(cursor.lastrowid)

	def get(self, course_id: int) -> Course:
		"""Return one course by ID, or raise ``LookupError`` if absent."""
		row = self.connection.execute(
			"SELECT id, code, name, instructor, credits FROM courses WHERE id = ?",
			(course_id,),
		).fetchone()
		if row is None:
			raise LookupError(f"Course {course_id} does not exist")
		return self._to_course(row)

	def list(self) -> list[Course]:
		"""Return all courses ordered by ID."""
		rows: Iterable[sqlite3.Row] = self.connection.execute(
			"SELECT id, code, name, instructor, credits FROM courses ORDER BY id"
		)
		return [self._to_course(row) for row in rows]

	def update(
		self,
		course_id: int,
		*,
		code: str,
		name: str,
		instructor: str,
		credits: int,
	) -> Course:
		"""Update a course and return it, or raise ``LookupError`` if absent."""
		cursor = self.connection.execute(
			"""
			UPDATE courses
			SET code = ?, name = ?, instructor = ?, credits = ?
			WHERE id = ?
			""",
			(code, name, instructor, credits, course_id),
		)
		self.connection.commit()
		if cursor.rowcount == 0:
			raise LookupError(f"Course {course_id} does not exist")
		return self.get(course_id)

	def delete(self, course_id: int) -> None:
		"""Delete a course, or raise ``LookupError`` if absent."""
		cursor = self.connection.execute(
			"DELETE FROM courses WHERE id = ?", (course_id,)
		)
		self.connection.commit()
		if cursor.rowcount == 0:
			raise LookupError(f"Course {course_id} does not exist")

	def close(self) -> None:
		"""Close the database connection."""
		self.connection.close()

	def __enter__(self) -> "CourseRepository":
		return self

	def __exit__(self, *_: object) -> None:
		self.close()
