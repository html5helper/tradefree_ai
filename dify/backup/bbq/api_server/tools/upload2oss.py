import os
import oss2
from typing import Optional

class OSSUploader:
    """阿里云OSS上传工具类"""
    
    def __init__(self, 
                #  access_key_id: str,
                #  access_key_secret: str,
                 endpoint: str,
                 bucket_name: str):
        """
        初始化OSS上传器
        
        Args:
            access_key_id: 阿里云AccessKeyId
            access_key_secret: 阿里云AccessKeySecret
            endpoint: OSS访问域名
            bucket_name: OSS存储空间名称
        """
        access_key_id = os.getenv('OSS_ACCESS_KEY_ID')
        access_key_secret = os.getenv('OSS_ACCESS_KEY_SECRET')

        if not access_key_id or not access_key_secret:
            raise ValueError("Access Key ID and Secret must be set as environment variables")
        self.auth = oss2.Auth(access_key_id, access_key_secret)
        self.bucket = oss2.Bucket(self.auth, endpoint, bucket_name)
        
    def upload_file(self,
                    local_file_path: str,
                    oss_file_path: Optional[str] = None,
                    headers: Optional[dict] = None) -> str:
        """
        上传文件到OSS
        
        Args:
            local_file_path: 本地文件路径
            oss_file_path: OSS上的文件路径,默认使用本地文件名
            headers: 上传时的HTTP头部,可选
            
        Returns:
            str: 文件在OSS上的路径
        """
        if not os.path.exists(local_file_path):
            raise FileNotFoundError(f"本地文件不存在: {local_file_path}")
            
        if oss_file_path is None:
            oss_file_path = os.path.basename(local_file_path)
            
        # 上传文件
        with open(local_file_path, 'rb') as f:
            self.bucket.put_object(oss_file_path, f, headers=headers)
            
        # 返回OSS路径
        return oss_file_path
        
    def upload_bytes(self,
                    file_content: bytes,
                    oss_file_path: str,
                    headers: Optional[dict] = None) -> str:
        """
        上传二进制内容到OSS
        
        Args:
            file_content: 文件二进制内容
            oss_file_path: OSS上的文件路径
            headers: 上传时的HTTP头部,可选
            
        Returns:
            str: 文件在OSS上的路径
        """
        self.bucket.put_object(oss_file_path, file_content, headers=headers)
        return oss_file_path

# 使用示例:
"""
# 创建上传器实例
uploader = OSSUploader(
    access_key_id='your_access_key_id',
    access_key_secret='your_access_key_secret', 
    endpoint='oss-cn-beijing.aliyuncs.com',
    bucket_name='your-bucket-name'
)

# 上传本地文件
url = uploader.upload_file(
    local_file_path='./test.jpg',
    oss_file_path='images/test.jpg'
)

# 上传二进制内容
content = b'Hello World'
url = uploader.upload_bytes(
    file_content=content,
    oss_file_path='test.txt'
)
"""
