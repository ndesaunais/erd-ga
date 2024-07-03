#!/usr/bin/python
# -*- coding: utf-8 -*-

import click
from click import File
from mermaid.erdiagram import Entity, ERDiagram, Link
from sqlalchemy import Column, MetaData, Table, create_engine
from sqlalchemy.engine import Engine


def to_attribute(column: Column) -> list[str]:
    attr = [column.type.__visit_name__]
    if column.primary_key:
        if len(column.foreign_keys) > 0:
            attr.extend(["PK,FK"])
        else:
            attr.append("PK")
    elif len(column.foreign_keys) > 0:
        attr.append("FK")
    elif column.unique:
        attr.append("UK")

    if column.comment:
        attr.append(column.comment)

    if column.nullable:
        attr.append("nullable")

    if column.index:
        attr.append("indexed")

    return attr


def to_entity(table: Table) -> Entity:
    attributes = {column.name: to_attribute(column) for column in table.columns}
    return Entity(table.name, attributes)


def sql_to_mermaid(metadata: MetaData) -> ERDiagram:
    links = []
    entities = {table.name: to_entity(table) for table in metadata.tables.values()}

    for table in metadata.tables.values():
        for column in table.columns:
            for fk in column.foreign_keys:
                end_card = "zero-or-one" if column.unique else "zero-or-more"
                left_table, left_column = fk.target_fullname.split(".")
                if left_table not in metadata.tables:
                    continue
                lcolumn = metadata.tables[left_table].columns[left_column]
                origin_card = (
                    "exactly-one"
                    if lcolumn.unique or lcolumn.primary_key
                    else "zero-or-more"
                )
                links.append(
                    Link(
                        origin=entities[left_table],
                        end=entities[table.name],
                        origin_cardinality=origin_card,
                        end_cardinality=end_card,
                        label=column.name,
                    )
                )

    return ERDiagram("bli", entities.values(), links)


@click.command()
@click.option(
    "-u",
    "--url",
    required=True,
    help="The full database url as in postgresql://user:passwd@localhost:5432/database",
)
@click.option(
    "-o",
    "--output",
    required=True,
    type=File("w"),
    help="The output path where to save the generated mermaid file",
)
def erd_dump(url: str, output):
    engine: Engine = create_engine(url)
    metadata = MetaData()
    metadata.reflect(bind=engine)

    er_diag = sql_to_mermaid(metadata)

    # TODO: manual removal of title
    _, _, script = er_diag.script.split("---")
    output.write(script)


if __name__ == "__main__":
    erd_dump()
