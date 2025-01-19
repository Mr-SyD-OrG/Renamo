import motor.motor_asyncio
from config import Config
from .utils import send_log

class Database:

    def __init__(self, uri, database_name):
        self._client = motor.motor_asyncio.AsyncIOMotorClient(uri)
        self.madflixbotz = self._client[database_name]
        self.col = self.madflixbotz.user
        self.grp = self.madflixbotz.groups

    def new_group(self, id, title):
        return dict(
            id = id,
            title = title,
            chat_status=dict(
                is_disabled=False,
                reason="",
            ),
        )

    def new_user(self, id):
        return dict(
            _id=int(id),                                   
            file_id=None,
            caption=None,
            dump=int(id),
            prefix=None,
            suffix=None,
            sydd=None,
            syddd=None,
            metadata_code=""" -map 0 -c:s copy -c:a copy -c:v copy -metadata title="Powered By:- " -metadata author="@" -metadata:s:s title="Subtitled By :- @" -metadata:s:a title="By :- @" -metadata:s:v title="By:@""",
            topic=None,
            sydson="True",
            format_template=None  # Add this line for the format template
        )

    async def add_user(self, b, m):
        u = m.from_user
        if not await self.is_user_exist(u.id):
            user = self.new_user(u.id)
            await self.col.insert_one(user)            
            await send_log(b, u)


    async def add_ser(self, id, name):
        user = self.new_user(id, name)
        await self.col.insert_one(user)


    async def add_chat(self, chat, title):
        chat = self.new_group(chat, title)
        await self.grp.insert_one(chat)
    

    async def get_chat(self, chat):
        chat = await selfrequests
        d_one({'id':int(chat)})
        return False if not chat else chat.get('chat_status')
    

    
    async def is_user_exist(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return bool(user)

    async def total_users_count(self):
        count = await self.col.count_documents({})
        return count

    async def get_all_users(self):
        all_users = self.col.find({})
        return all_users

    async def delete_user(self, user_id):
        await self.col.delete_many({'_id': int(user_id)})
    
    async def set_thumbnail(self, id, file_id):
        await self.col.update_one({'_id': int(id)}, {'$set': {'file_id': file_id}})

    async def get_thumbnail(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('file_id', None)

    async def set_caption(self, id, caption):
        await self.col.update_one({'_id': int(id)}, {'$set': {'caption': caption}})

    async def get_caption(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('caption', None)

    async def set_format_template(self, id, format_template):
        await self.col.update_one({'_id': int(id)}, {'$set': {'format_template': format_template}})

    async def get_format_template(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('format_template', None)
        
    async def set_media_preference(self, id, media_type):
        await self.col.update_one({'_id': int(id)}, {'$set': {'media_type': media_type}})
        
    async def get_media_preference(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('media_type', None)

    async def set_suffix(self, id, suffix):
        await self.col.update_one({'_id': int(id)}, {'$set': {'suffix': suffix}})

    async def set_metadata(self, id, bool_meta):
        await self.col.update_one({'_id': int(id)}, {'$set': {'metadata': bool_meta}})

    async def get_metadata(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('metadata', None)

    async def set_metadata_code(self, id, metadata_code):
        await self.col.update_one({'_id': int(id)}, {'$set': {'metadata_code': metadata_code}})

    async def get_metadata_code(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('metadata_code', None)
        
    async def get_suffix(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('suffix', None)

    async def set_dump(self, id, dump: int):
        await self.col.update_one({'_id': int(id)}, {'$set': {'dump': int(dump)}})

    async def set_rep(self, id, sydd, syddd):
        await self.col.update_one(
            {'_id': int(id)},  # Find the document by its ID
            {'$set': {'sydd': sydd, 'syddd': syddd}}  # Update 'sydd' and 'syddd' fields
        )

    async def get_dump(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('dump', int(id))

    async def set_sydson(self, id, syd):
        await self.col.update_one({'_id': int(id)}, {'$set': {'sydson': syd}})

    async def set_topic(self, id, syd: int):
        await self.col.update_one({'_id': int(id)}, {'$set': {'topic': int(syd)}})
    
    async def get_sydson(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('sydson', id)
    
    async def get_topic(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('topic', int(id))

    async def get_rep(self, id):
        user = await self.col.find_one({'_id': int(id)})
        if user:  # Check if the document exists
            return {
                'sydd': user.get('sydd', ""),   # Default to an empty string if 'sydd' is not found
                'syddd': user.get('syddd', "")  # Default to an empty string if 'syddd' is not found
            }
        return {'sydd': "", 'syddd': ""}  # Default return if the document doesn't exist


    async def set_prefix(self, id, prefix):
        await self.col.update_one({'_id': int(id)}, {'$set': {'prefix': prefix}})

    async def get_prefix(self, id):
        user = await self.col.find_one({'_id': int(id)})
        return user.get('prefix', None)




madflixbotz = Database(Config.DB_URL, Config.DB_NAME)
db = madflixbotz


# Jishu Developer 
# Don't Remove Credit 🥺
# Telegram Channel @Madflix_Bots
# Developer @JishuDeveloper
