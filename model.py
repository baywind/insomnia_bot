import sqlalchemy
import datetime
from sqlalchemy.ext.declarative import declarative_base
from texts import DEFAULT_GREETING

SqlAlchemyBase = declarative_base()


class BotModel(SqlAlchemyBase):
    __tablename__ = 'registered_bot'

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    name = sqlalchemy.Column(sqlalchemy.String, nullable=False)
    owner_id = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=False)
    target_chat_id = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=True)
    timezone = sqlalchemy.Column(sqlalchemy.SmallInteger, nullable=False, default=3)

    start_text = sqlalchemy.Column(sqlalchemy.String, nullable=True, default=DEFAULT_GREETING)

    created_date = sqlalchemy.Column(sqlalchemy.DateTime,
                                     default=datetime.datetime.now)

    # news = sqlalchemy.orm.relation("MessageLog", back_populates='bot')

    def __repr__(self):
        return f'<bot: @{self.name}>'

    def get_session(self) -> sqlalchemy.orm.Session:
        return sqlalchemy.orm.Session.object_session(self)


class MessageLog(SqlAlchemyBase):
    EMPTY_NAME = "<noname>"
    __tablename__ = 'message_log'
    REQUEST = 1
    RESPONSE = 2
    TECH = 0

    id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True, autoincrement=True)
    direction = sqlalchemy.Column(sqlalchemy.Integer, nullable=False, default=0)

    ext_user_id = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=True)
    int_user_id = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=True)

    ext_user_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)
    int_user_name = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    timestamp = sqlalchemy.Column(sqlalchemy.BigInteger, nullable=False, index=True)
    # content = sqlalchemy.Column(sqlalchemy.String, nullable=True)

    bot_id = sqlalchemy.Column(sqlalchemy.Integer,
                               sqlalchemy.ForeignKey("registered_bot.id"), index=True)
    bot = sqlalchemy.orm.relationship('BotInstance')

    def __str__(self):
        date = datetime.datetime.fromtimestamp(self.timestamp, self.bot.tz())\
            .strftime('%d.%m %H:%M:%S')
        int_user_name = self.int_user_name or self.EMPTY_NAME
        ext_user_name = self.ext_user_name or self.EMPTY_NAME
        if self.direction == 0:
            return f'{date} {int_user_name} # {ext_user_name}'
        elif self.direction == 1:
            return f'{date} {ext_user_name} -> {self.bot.name}'
        elif self.direction == 2:
            return f'{date} {ext_user_name} <- {int_user_name}'

    @classmethod
    def format_log(cls, log, entities):
        result = []  # '\n'.join(map(str, log))
        offset = 0
        for record in log:
            row = str(record)
            name: str = record.ext_user_name or record.EMPTY_NAME
            if not name.startswith('@'):
                try:
                    entities.append(
                        {
                            "offset": offset + row.index(name),
                            "length": len(name),
                            "type": "text_mention",
                            "user": {
                                "id": record.ext_user_id,
                                "is_bot": False
                            }
                        }
                    )
                except ValueError:
                    pass
            result.append(row)
            offset += len(row) + 1
        return '\n'.join(result)
