from neomodel import db, config
import logging
from dotenv import load_dotenv
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


load_dotenv()

db_username = os.getenv("DB_USER")
db_password = os.getenv("DB_PASSWORD")

# Подключение к базе Neo4j
config.DATABASE_URL = f"bolt://{db_username}:{db_password}@localhost:7687"
config.USERNAME = os.getenv("DB_USER")
config.PASSWORD = os.getenv("DB_PASSWORD")

class Queries:

    @staticmethod
    def get_all_nodes():
        logger.info("Извлечение всех узлов с их идентификаторами и метками.")
        # Запрос для получения всех узлов и их меток
        query = "MATCH (n) RETURN id(n) AS id, labels(n)[0] AS label"
        result, _ = db.cypher_query(query)  # Возвращаем результат и пустое значение
        return [{"node_id": record[0], "label": record[1]} for record in result]

    @staticmethod
    def get_node_and_relations(node_id: int):
        logger.info(f"Извлечение узла {node_id}, его метки и связей.")
        # Запрос для получения узла по node_id и всех его связей
        query = """
        MATCH (n)-[r]->(m)
        WHERE n.node_id = $node_id
        RETURN n, r, m, labels(n)[0] AS label
        """
        result, _ = db.cypher_query(query, {"node_id": node_id})  # Запуск запроса и передача параметра
        logger.info(f"Query result: {result}")

        node_data = {}
        relationships = []

        if result:
            # Извлечение данных узла из результата
            node = result[0][0]  # Это будет объект узла (Node)
            node_data = {
                "node_id": result[0][0]['node_id'],  # Доступ к node_id через индекс
                "label": result[0][3],  # Извлекаем метку из результата запроса
                "properties": dict(result[0][0])  # Извлекаем все свойства узла через dict
            }

            # Обработка связей
            for record in result:
                relationship = record[1]  # Это будет объект связи (Relationship)
                target_node = record[2]  # Целевой узел в связи
                relationships.append({
                    "relationship_type": relationship.__class__.__name__,  # Тип связи
                    "target_node_id": target_node['node_id'],  # Доступ к node_id целевого узла через индекс
                    "target_node_label": target_node[3],  # Метка целевого узла
                    "properties": dict(target_node)  # Свойства целевого узла
                })

        return {
            "node": node_data,
            "relationships": relationships
        }

    @staticmethod
    def insert_node_and_relationships(node, relationships):
        logger.info(f"Процедура добавления узла... ")
        node_query = """
        CREATE (n:{label} {{
            node_id: $id, name: $name, screen_name: $screen_name,
            sex: $sex, home_town: $home_town
        }})
        """
        # Выполнение запроса для вставки узла
        db.cypher_query(node_query.format(label=node.label), {
            "id": node.node_id,
            "name": node.name,
            "screen_name": node.screen_name,
            "sex": node.sex,
            "home_town": node.home_town
        })

        if relationships:
            rel_query = """
            UNWIND $relationships AS rel
            MATCH (n {node_id: $node_id}), (m {node_id: rel.end_node_id})
            CREATE (n)-[r:REL_TYPE {id: rel.id}]->(m)
            """
            # Добавление связей для узла
            rel_data = [
                {"id": rel.id, "end_node_id": rel.end_node_id, "type": rel.type}
                for rel in relationships
            ]
            db.cypher_query(rel_query, {
                "node_id": node.node_id,
                "relationships": rel_data
            })
        return "Узел и связи добавлены."

    @staticmethod
    def delete_node_and_relationships(node_id: int):
        logger.info(f"Удаление узла {node_id} вместе с его связями. ")
        # Запрос для удаления всех связей и узла
        query = """
        MATCH (n)-[r]-(m)
        WHERE id(n) = $node_id
        DELETE r, n
        """
        # Выполнение запроса на удаление
        db.cypher_query(query, {"node_id": node_id})
        logger.info(f"Узел {node_id} успешно удален.")
        return "Узел удален."