import unittest
from models import Model
from config.db import get_engine
from models.user import User

class ModelTest(unittest.TestCase):
    def setUp(self):
        self.model = Model()

    def tearDown(self) -> None:
        self.model.delete()

    def test_create_user(self):
        user_id = self.model.create_user(123456789)
        self.assertIsInstance(user_id, int)

    def test_get_users(self):
        users = self.model.get_users()
        self.assertIsInstance(users, list)
        self.assertEqual(users, [])

    def test_creating_user_then_getting_user(self):
        user_id = self.model.create_user(123456789)
        user = self.model.get_users()[0]
        self.assertEqual(user.id, user_id)
        self.assertEqual(user.discord_id, 123456789)

    def test_get_user_by_id(self):
        user_id = self.model.create_user(123456789)
        user = self.model.get_user_by_id(user_id)
        self.assertEqual(user.id, user_id)
        self.assertEqual(user.discord_id, 123456789)

    def test_get_user_by_id_with_multiple_users(self):
        user_id1 = self.model.create_user(123456789)
        user_id2 = self.model.create_user(987654321)
        user_id3 = self.model.create_user(213456789)
        user = self.model.get_user_by_id(user_id2)
        self.assertEqual(user.id, user_id2)
        self.assertEqual(user.discord_id, 987654321)

    def test_get_user_by_id_with_no_users(self):
        with self.assertRaises(Exception):
            self.model.get_user_by_id(1)

    def test_update_user(self):
        user_id = self.model.create_user(123456789)
        self.model.update_user(user_id, 987654321)
        user = self.model.get_user_by_id(user_id)
        self.assertEqual(user.discord_id, 987654321)

    def test_delete_user(self):
        user_id = self.model.create_user(123456789)
        self.model.delete_user(user_id)
        users = self.model.get_users()
        self.assertEqual(users, [])

    def test_create_server(self):
        server_id = self.model.create_server(123456789)
        self.assertIsInstance(server_id, int)

    def test_get_servers(self):
        servers = self.model.get_servers()
        self.assertIsInstance(servers, list)
        self.assertEqual(servers, [])

    def test_creating_server_then_getting_server(self):
        server_id = self.model.create_server(123456789)
        server = self.model.get_servers()[0]
        self.assertEqual(server.id, server_id)
        self.assertEqual(server.discord_id, 123456789)
    
    def test_get_server_by_id(self):
        server_id = self.model.create_server(123456789)
        server = self.model.get_server_by_id(server_id)
        self.assertEqual(server.id, server_id)
        self.assertEqual(server.discord_id, 123456789)

    def test_get_server_by_id_with_multiple_servers(self):
        server_id1 = self.model.create_server(123456789)
        server_id2 = self.model.create_server(987654321)
        server_id3 = self.model.create_server(213456789)
        server = self.model.get_server_by_id(server_id2)
        self.assertEqual(server.id, server_id2)
        self.assertEqual(server.discord_id, 987654321)

    def test_get_server_by_id_with_no_servers(self):
        with self.assertRaises(Exception):
            self.model.get_server_by_id(1)

    def test_update_server(self):
        server_id = self.model.create_server(123456789)
        self.model.update_server(server_id, 987654321)
        server = self.model.get_server_by_id(server_id)
        self.assertEqual(server.discord_id, 987654321)

    def test_delete_server(self):
        server_id = self.model.create_server(123456789)
        self.model.delete_server(server_id)
        servers = self.model.get_servers()
        self.assertEqual(servers, [])

    def test_create_channel(self):
        server_id = self.model.create_server(123456789)
        channel_id = self.model.create_channel(123456789, True, server_id)
        self.assertIsInstance(channel_id, int)

    def test_get_channels(self):
        channels = self.model.get_channels()
        self.assertIsInstance(channels, list)
        self.assertEqual(channels, [])

    def test_creating_channel_then_getting_channel(self):
        server_id = self.model.create_server(123456789)
        channel_id = self.model.create_channel(123456789, True, server_id)
        channel = self.model.get_channels()[0]
        self.assertEqual(channel.id, channel_id)
        self.assertEqual(channel.discord_id, 123456789)
        self.assertEqual(channel.enabled, True)
        self.assertEqual(channel.server_id, server_id)

    def test_get_channel_by_id(self):
        server_id = self.model.create_server(123456789)
        channel_id = self.model.create_channel(123456789, True, server_id)
        channel = self.model.get_channel_by_id(channel_id)
        self.assertEqual(channel.id, channel_id)
        self.assertEqual(channel.discord_id, 123456789)
        self.assertEqual(channel.enabled, True)
        self.assertEqual(channel.server_id, server_id)

    def test_get_channel_by_id_with_multiple_channels(self):
        server_id = self.model.create_server(123456789)
        channel_id1 = self.model.create_channel(123456789, True, server_id)
        channel_id2 = self.model.create_channel(987654321, False, server_id)
        channel_id3 = self.model.create_channel(213456789, True, server_id)
        channel = self.model.get_channel_by_id(channel_id2)
        self.assertEqual(channel.id, channel_id2)
        self.assertEqual(channel.discord_id, 987654321)
        self.assertEqual(channel.enabled, False)
        self.assertEqual(channel.server_id, server_id)

    def test_get_channel_by_id_with_no_channels(self):
        with self.assertRaises(Exception):
            self.model.get_channel_by_id(1)

    def test_update_channel(self):
        server_id = self.model.create_server(123456789)
        channel_id = self.model.create_channel(123456789, True, server_id)
        self.model.update_channel(channel_id, 987654321, False, server_id)
        channel = self.model.get_channel_by_id(channel_id)
        self.assertEqual(channel.discord_id, 987654321)
        self.assertEqual(channel.enabled, False)
        self.assertEqual(channel.server_id, server_id)

    def test_delete_channel(self):
        server_id = self.model.create_server(123456789)
        channel_id = self.model.create_channel(123456789, True, server_id)
        self.model.delete_channel(channel_id)
        channels = self.model.get_channels()
        self.assertEqual(channels, [])

    def test_create_tag(self):
        tag_id = self.model.create_tag('test')
        self.assertIsInstance(tag_id, int)

    def test_get_tags(self):
        tags = self.model.get_tags()
        self.assertIsInstance(tags, list)
        self.assertEqual(tags, [])
    
    def test_creating_tag_then_getting_tag(self):
        tag_id = self.model.create_tag('test')
        tag = self.model.get_tags()[0]
        self.assertEqual(tag.id, tag_id)
        self.assertEqual(tag.name, 'test')
    
    def test_get_tag_by_id(self):
        tag_id = self.model.create_tag('test')
        tag = self.model.get_tag_by_id(tag_id)
        self.assertEqual(tag.id, tag_id)
        self.assertEqual(tag.name, 'test')

    def test_get_tag_by_id_with_multiple_tags(self):
        tag_id1 = self.model.create_tag('test1')
        tag_id2 = self.model.create_tag('test2')
        tag_id3 = self.model.create_tag('test3')
        tag = self.model.get_tag_by_id(tag_id2)
        self.assertEqual(tag.id, tag_id2)
        self.assertEqual(tag.name, 'test2')

    def test_get_tag_by_id_with_no_tags(self):
        with self.assertRaises(Exception):
            self.model.get_tag_by_id(1)
        
    def test_update_tag(self):
        tag_id = self.model.create_tag('test')
        self.model.update_tag(tag_id, 'test2')
        tag = self.model.get_tag_by_id(tag_id)
        self.assertEqual(tag.name, 'test2')

    def test_delete_tag(self):
        tag_id = self.model.create_tag('test')
        self.model.delete_tag(tag_id)
        tags = self.model.get_tags()
        self.assertEqual(tags, [])

    def test_create_message(self):
        user_id = self.model.create_user(123456789)
        server_id = self.model.create_server(123456789)
        channel_id = self.model.create_channel(123456789, True, server_id)
        message_id = self.model.create_message(42134512, channel_id, user_id, [])
        self.assertIsInstance(message_id, int)

    def test_get_messages(self):
        messages = self.model.get_messages()
        self.assertIsInstance(messages, list)
        self.assertEqual(messages, [])

    def test_creating_message_then_getting_message(self):
        user_id = self.model.create_user(123456789)
        server_id = self.model.create_server(123456789)
        channel_id = self.model.create_channel(123456789, True, server_id)
        message_id = self.model.create_message(42134512, channel_id, user_id, [])
        message = self.model.get_messages()[0]
        self.assertEqual(message.id, message_id)
        self.assertEqual(message.discord_id, 42134512)
        self.assertEqual(message.channel_id, channel_id)
        self.assertEqual(message.user_id, user_id)
        self.assertEqual(message.tags, [])

    def test_get_message_by_id(self):
        user_id = self.model.create_user(123456789)
        server_id = self.model.create_server(123456789)
        channel_id = self.model.create_channel(123456789, True, server_id)
        message_id = self.model.create_message(42134512, channel_id, user_id, [])
        message = self.model.get_message_by_id(message_id)
        self.assertEqual(message.id, message_id)
        self.assertEqual(message.discord_id, 42134512)
        self.assertEqual(message.channel_id, channel_id)
        self.assertEqual(message.user_id, user_id)
        self.assertEqual(message.tags, [])

    def test_get_message_by_id_with_multiple_messages(self):
        user_id = self.model.create_user(123456789)
        server_id = self.model.create_server(123456789)
        channel_id = self.model.create_channel(123456789, True, server_id)
        message_id1 = self.model.create_message(42134512, channel_id, user_id, [])
        message_id2 = self.model.create_message(42134513, channel_id, user_id, [])
        message_id3 = self.model.create_message(42134514, channel_id, user_id, [])
        message = self.model.get_message_by_id(message_id2)
        self.assertEqual(message.id, message_id2)
        self.assertEqual(message.discord_id, 42134513)
        self.assertEqual(message.channel_id, channel_id)
        self.assertEqual(message.user_id, user_id)
        self.assertEqual(message.tags, [])

    def test_get_message_by_id_with_no_messages(self):
        with self.assertRaises(Exception):
            self.model.get_message_by_id(1)

    def test_update_message(self):
        user_id = self.model.create_user(123456789)
        server_id = self.model.create_server(123456789)
        channel_id = self.model.create_channel(123456789, True, server_id)
        message_id = self.model.create_message(42134512, channel_id, user_id, [])
        self.model.update_message(message_id, 42134513, channel_id, user_id, [])
        message = self.model.get_message_by_id(message_id)
        self.assertEqual(message.discord_id, 42134513)
        self.assertEqual(message.channel_id, channel_id)
        self.assertEqual(message.user_id, user_id)
        self.assertEqual(message.tags, [])

    def test_delete_message(self):
        user_id = self.model.create_user(123456789)
        server_id = self.model.create_server(123456789)
        channel_id = self.model.create_channel(123456789, True, server_id)
        message_id = self.model.create_message(42134512, channel_id, user_id, [])
        self.model.delete_message(message_id)
        messages = self.model.get_messages()
        self.assertEqual(messages, [])

    def test_create_message_with_tag(self):
        user_id = self.model.create_user(123456789)
        server_id = self.model.create_server(123456789)
        channel_id = self.model.create_channel(123456789, True, server_id)
        tag_id = self.model.create_tag('test')
        tag = self.model.get_tag_by_id(tag_id)
        message_id = self.model.create_message(42134512, channel_id, user_id, [tag])
        message = self.model.get_message_by_id(message_id)
        self.assertEqual(message.tags[0].id, tag_id)
        self.assertEqual(message.tags[0].name, 'test')

    def test_create_message_with_multiple_tags(self):
        user_id = self.model.create_user(123456789)
        server_id = self.model.create_server(123456789)
        channel_id = self.model.create_channel(123456789, True, server_id)
        tag_id1 = self.model.create_tag('test1')
        tag_id2 = self.model.create_tag('test2')
        tag_id3 = self.model.create_tag('test3')
        tag1 = self.model.get_tag_by_id(tag_id1)
        tag2 = self.model.get_tag_by_id(tag_id2)
        tag3 = self.model.get_tag_by_id(tag_id3)
        message_id = self.model.create_message(42134512, channel_id, user_id, [tag1, tag2, tag3])
        message = self.model.get_message_by_id(message_id)
        self.assertEqual(message.tags[0].id, tag_id1)
        self.assertEqual(message.tags[0].name, 'test1')
        self.assertEqual(message.tags[1].id, tag_id2)
        self.assertEqual(message.tags[1].name, 'test2')
        self.assertEqual(message.tags[2].id, tag_id3)
        self.assertEqual(message.tags[2].name, 'test3')

    def test_create_attatchment(self):
        user_id = self.model.create_user(123456789)
        server_id = self.model.create_server(123456789)
        channel_id = self.model.create_channel(123456789, True, server_id)
        message_id = self.model.create_message(42134512, channel_id, user_id, [])
        attatchment_id = self.model.create_attachment(42134432, message_id)
        self.assertIsInstance(attatchment_id, int)

    def test_get_attatchments(self):
        attatchments = self.model.get_attachments()
        self.assertIsInstance(attatchments, list)
        self.assertEqual(attatchments, [])

    def test_creatingattachment_then_getting_attatchment(self):
        user_id = self.model.create_user(123456789)
        server_id = self.model.create_server(123456789)
        channel_id = self.model.create_channel(123456789, True, server_id)
        message_id = self.model.create_message(42134512, channel_id, user_id, [])
        attatchment_id = self.model.create_attachment(42134432, message_id)
        attatchment = self.model.get_attachments()[0]
        self.assertEqual(attatchment.id, attatchment_id)
        self.assertEqual(attatchment.discord_id, 42134432)
        self.assertEqual(attatchment.message_id, message_id)
    
    def test_get_attachments_by_id(self):
        user_id = self.model.create_user(123456789)
        server_id = self.model.create_server(123456789)
        channel_id = self.model.create_channel(123456789, True, server_id)
        message_id = self.model.create_message(42134512, channel_id, user_id, [])
        attatchment_id = self.model.create_attachment(42134432, message_id)
        attatchment = self.model.get_attachment_by_id(attatchment_id)
        self.assertEqual(attatchment.id, attatchment_id)
        self.assertEqual(attatchment.discord_id, 42134432)
        self.assertEqual(attatchment.message_id, message_id)

    def test_get_attachment_by_id_with_multiple_attachments(self):
        user_id = self.model.create_user(123456789)
        server_id = self.model.create_server(123456789)
        channel_id = self.model.create_channel(123456789, True, server_id)
        message_id = self.model.create_message(42134512, channel_id, user_id, [])
        attatchment_id1 = self.model.create_attachment(42134432, message_id)
        attatchment_id2 = self.model.create_attachment(42134433, message_id)
        attatchment_id3 = self.model.create_attachment(42134434, message_id)
        attatchment = self.model.get_attachment_by_id(attatchment_id2)
        self.assertEqual(attatchment.id, attatchment_id2)
        self.assertEqual(attatchment.discord_id, 42134433)
        self.assertEqual(attatchment.message_id, message_id)

    def test_get_attachment_by_id_with_no_attachments(self):
        with self.assertRaises(Exception):
            self.model.get_attachment_by_id(1)

    def test_update_attachment(self):
        user_id = self.model.create_user(123456789)
        server_id = self.model.create_server(123456789)
        channel_id = self.model.create_channel(123456789, True, server_id)
        message_id = self.model.create_message(42134512, channel_id, user_id, [])
        attatchment_id = self.model.create_attachment(42134432, message_id)
        self.model.update_attachment(attatchment_id, 42134433, message_id)
        attatchment = self.model.get_attachment_by_id(attatchment_id)
        self.assertEqual(attatchment.discord_id, 42134433)
        self.assertEqual(attatchment.message_id, message_id)

    def test_delete_attachment(self):
        user_id = self.model.create_user(123456789)
        server_id = self.model.create_server(123456789)
        channel_id = self.model.create_channel(123456789, True, server_id)
        message_id = self.model.create_message(42134512, channel_id, user_id, [])
        attatchment_id = self.model.create_attachment(42134432, message_id)
        self.model.delete_attachment(attatchment_id)
        attatchments = self.model.get_attachments()
        self.assertEqual(attatchments, [])
    