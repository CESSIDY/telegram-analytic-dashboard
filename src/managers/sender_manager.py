from telethon.tl import functions
import logging

logger = logging.getLogger(__name__)


class SenderManager:

    def __init__(self, client, comments_loader):
        self.client = client
        self.comments_loader = comments_loader

    async def try_send_comment_with_retry(self, peer, message, reply_to_msg_id, media=None):
        """
        Method gonna send media comment to post, and if it's didn't work, then we try send some text comment
        (because some times channel no allow sending media files)
        """
        if media:
            result = await self.send_media_comment(media=media,
                                                   peer=peer,
                                                   message=message,
                                                   reply_to_msg_id=reply_to_msg_id)
            if result:
                return result

            logger.info("Try re-send text message")
            comment = self.comments_loader.get_text_comment()
            if comment:
                message = comment.message

        return await self.send_text_comment(peer=peer,
                                            message=message,
                                            reply_to_msg_id=reply_to_msg_id)

    async def send_media_comment(self, media, peer, message, reply_to_msg_id):
        try:
            result = await self.client(functions.messages.SendMediaRequest(peer=peer,
                                                                           media=media,
                                                                           message=message,
                                                                           reply_to_msg_id=reply_to_msg_id))
            return result
        except Exception as e:
            logger.warning(e)
        return

    async def send_text_comment(self, peer, message, reply_to_msg_id):
        try:
            result = await self.client(functions.messages.SendMessageRequest(peer=peer,
                                                                             message=message,
                                                                             reply_to_msg_id=reply_to_msg_id))
            return result
        except Exception as e:
            logger.warning(e)
        return
