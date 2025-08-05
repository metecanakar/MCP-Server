## Modül 1 , Ders 1 
Stateless agent yapısı ve bir API call örneği

Yapılacaklar : 
* gerekli kütüphaneler kurulur : pip install flask
* stateless.py dosyası çalıştırılır : python stateless.py

Aşağıdaki şekilde çağrı atılır:
<pre>
curl -X POST http://localhost:5000/chat \
     -H "Content-Type: application/json" \
     -d '{"message": "Merhaba, adım Ahmet"}'
</pre>

<pre>
curl -X POST -H "Content-Type: application/json" -d '{"message": "Merhaba benim adım Elif"}' http://127.0.0.1:5000/chat
</pre>

<pre>
curl -X POST -H "Content-Type: application/json" -d '{"message": "Benim adım neydi?"}' http://127.0.0.1:5000/chat
</pre>


Çıktıları yorumlayınız. 