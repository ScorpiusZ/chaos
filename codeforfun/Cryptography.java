import javax.crypto.Cipher;
import javax.crypto.SecretKey;
import javax.crypto.SecretKeyFactory;
import javax.crypto.spec.DESKeySpec; 
import javax.crypto.spec.IvParameterSpec;
import sun.misc.BASE64Decoder;   
import sun.misc.BASE64Encoder; 

/**
 * @author Jesons.jiang
 * @version V1.0
 * @since 2010-09-30
 */
public class Cryptography {
	public Cryptography(){}
	
	private final static String DES = "DES/CBC/PKCS5Padding"; //DES/ECB/PKCS5Padding
	private final static String Encoding = "UTF-8"; 
		
	/**
	 * DES加密字符串
	 * @param encryptString  待加密的字符串
	 * @param encryptKey   加密密钥,要求为8位
	 * @return 加密成功返回加密后的字符串，失败返回源串
	 */
	public static String EncryptDES(String encryptString, String encryptKey)
	{
		String ret = "";
		
		try
		{
	        // 从原始密匙数据创建DESKeySpec对象	        
	        byte[] key = encryptKey.getBytes(Encoding);
	        DESKeySpec dks = new DESKeySpec(key);
	
	        // 创建一个密匙工厂，然后用它把DESKeySpec转换成
	        // 一个SecretKey对象
	        SecretKeyFactory keyFactory = SecretKeyFactory.getInstance("DES");
	        SecretKey securekey = keyFactory.generateSecret(dks);
	
	        // Cipher对象实际完成加密操作
	        Cipher cipher = Cipher.getInstance(DES);
	
	        // 用密匙初始化Cipher对象
	        IvParameterSpec iv = new IvParameterSpec(new byte[8]);
	        cipher.init(Cipher.ENCRYPT_MODE, securekey, iv);
	        
	        // 获取数据并加密
	        byte[] src = encryptString.getBytes(Encoding);
	        src = cipher.doFinal(src); 
	        BASE64Encoder enc=new BASE64Encoder();
	        ret = enc.encode(src);
		}
		catch(Exception ex)
		{
			System.out.println(ex.getMessage());
			System.out.println(ex.getStackTrace());
			
			ret = encryptString;
		}
		return ret;
	}
	
	/**
	 * DES解密字符串
	 * @param decryptString 待解密的字符串
	 * @param decryptKey 解密密钥,要求为8位,和加密密钥相同
	 * @return 解密成功返回解密后的字符串，失败返源串
	 */
	 public static String DecryptDES(String decryptString, String decryptKey)
     {
		 String ret = "";
		 try
		 {	
	         // 从原始密匙数据创建一个DESKeySpec对象
	         byte[] key = decryptKey.getBytes(Encoding);
	         DESKeySpec dks = new DESKeySpec(key);
	
	         // 创建一个密匙工厂，然后用它把DESKeySpec对象转换成
	         // 一个SecretKey对象
	         SecretKeyFactory keyFactory = SecretKeyFactory.getInstance("DES");
	         SecretKey securekey = keyFactory.generateSecret(dks);
	
	         // Cipher对象实际完成解密操作
	         Cipher cipher = Cipher.getInstance(DES);
	
	         // 用密匙初始化Cipher对象
		     IvParameterSpec iv = new IvParameterSpec(new byte[8]);
	         cipher.init(Cipher.DECRYPT_MODE, securekey, iv);
	
	         //获取数据并解密
	         BASE64Decoder dnc = new BASE64Decoder();
	         byte[] src = dnc.decodeBuffer(decryptString);
	         src = cipher.doFinal(src);
	         ret = new String(src,0,src.length,Encoding);
		 }
		catch(Exception ex)
		{
			System.out.println(ex.getMessage());
			System.out.println(ex.getStackTrace());
			
			ret = decryptString;
		}
		 return ret;
     }

   public static void main(String[] args){
     String text = args[0];
     String key = args[1];
     System.out.print(EncryptDES(text,key));
   }
}

