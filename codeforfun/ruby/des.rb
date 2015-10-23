module Des
  require 'openssl'
  require 'base64'

  ALG='des-cbc'

  module_function
  def encrypt(str,key)
    cipher = OpenSSL::Cipher::Cipher.new(ALG)
    cipher.encrypt
    cipher.key = key
    result = cipher.update(str) + cipher.final
    Base64.encode64(result)
  end

  def decrypt(str,key)
    des = OpenSSL::Cipher::Cipher.new(ALG)
    des.decrypt
    des.key = key
    des.update(Base64.decode64(str)) + des.final
  end


  result = encrypt('123456','4B40A73D')
  p result
  p decrypt(result,'4B40A73D')

end

