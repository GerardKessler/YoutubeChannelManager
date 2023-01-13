# YoutubeKanal Yöneticisi
[Gerardo Késsler](http://gera.ar)  

Bu Eklenti, YouTube platformundaki favori kanallarınızı klavye kısayolları ve görünmeyen sanal basit bir arayüz ile yönetmenize imkan verir.  

## Eklenti Kısayolları:

* NVDA + Y; Görünmez arayüzü açar ve tekrar basıldığında kapatır.  
* Atanmamış; Panoda bulunan bir video bağlantısını kullanarak özel Web oynatıcısını etkinleştirir.

## Görünmez arayüzde bulunan kısayollar:

* escape; sanal arayüzü kapatır ve klavye kısayollarını varsayılan işlevlerine döndürür.
* sağ ok; sonraki kanala geçer.
* Sol ok; önceki kanala geçer.
* Aşağı ok; odaklanmış kanalda bir sonraki videoya geçer.
* Yukarı ok; odaklanmış kanalda önceki videoya geçer.
* Home tuşu; Odaklanmış kanalda ilk videoya gider.
* End tuşu; konumu, kanalın adını ve videonun izlenme sayısını söyler.
* n; yeni bir kanal eklemek için iletişim kutusunu açar.
* o; video bağlantısını varsayılan tarayıcıda açar.
* r; Ses bağlantısını özel bir web oynatıcısında açar.
* c; Video bağlantısını panoya kopyalar.
* t; Video başlığını panoya kopyalar.
* d; video bilgilerini alıp bir pencerede görüntüler.
* control + d; videoyu orijinal biçimde mevcut kullanıcının YoutubeDL klasörüne indirir.
* b; Veritabanındaki arama iletişim kutusunu etkinleştirir.
* Control + b; Genel arama iletişim kutusunu etkinleştirir.
* f5; Kanala eklenmiş yeni videolar olup olmadığını kontrol eder.
* s; Odaklanmış kanalın ayarlar penceresini açar.
* g; Genel Ayarlar penceresini etkinleştirir.
* Del tuşu; Odaklanmış kanalı siler ve ana pencereye geri döner.
* control + shift + Del tuşu; Veritabanını siler.
* f1; komut yardımını açar.

### kanal ekle:

Yeni bir kanal ekleyebilmek için:  
Varsayılan olarak atanmış NVDA + Y kısayol tuşuna basarak görünmez pencereyi açmamız ve n tuşuna basarak kanal ekleme alanına erişmemiz yeterli.  
Kanal adını ve adresini yazabileceğimiz iki yazma alanı doldurulduktan sonra Kanal ekleye basarak kanalın eklenmesini sağlayabiliyoruz.  
İki türde adres ekleyebiliyoruz:  

* genellikle aşağıdaki biçime sahip bir videonun bağlantısı:

    https://www.youtube.com/watch?v=IdDelVideo

* Bir kanalın bağlantısı:

    https://www.youtube.com/channel/IdDelCanal

İstenen video veya kanal adresi:  
Varsayılan tarayıcıda içerik açıldıktan sonra ALT+D veya CTRL+L ile adres alanına erişilir ve ardından da CTRL+C ile adres kopyalanır.  

Kanallar, Genel sonuçlar listesinden de eklenebilir. Bunun için tek yapmamız gereken arama yapmak ve eklemek istediğimiz kanalın videosuna gidip n tuşuna basmak.  

Kanal ekleme iletişim kutusu etkinleşecek, Youtube sitesinden otomatik olarak alınan bilgiler ile yazma alanları doldurulacak ve onayladığımızda veritabanımıza eklenecektir.  

### Otomatik güncelleyici:

Eklenti, kanalları favori olarak işaretlememize ve öngörülen bir zaman aralığında güncelleme kontrolünü etkinleştirmemize olanak tanır.  
Bir kanalı favori olarak işaretlemek veya işareti kaldırmak için:  

* Varsayılan olarak NVDA +Y olarak atanan hareketle sanal arayüzü etkinleştiriyoruz.
* Sol veya sağ oklarla istediğimiz kanalı seçiyoruz.
* s harfi ile kanal ayarları penceresini etkinleştiriyoruz.
* İlgili kutuyu işaretliyoruz ve konfigürasyonu kaydediyoruz.

Favori kanallardaki güncellemelerin kontrol edilmesi varsayılan olarak kapalıdır. Değiştirmek için şu adımları izliyoruz:  

* Varsayılan olarak atanmış NVDA+Y kısayoluna basarak sanal arayüzü açıyoruz.
* Genel Ayarlar penceresini g harfine basarak etkinleştiriyoruz.
* Sekme tuşu ile ilerleyerek ilgili alana geliyor ve dilediğimiz aralığı seçiyoruz.
* Ayarları kaydetmek için, Ayarları kaydet butonuna tıklıyoruz.

Güncelleme bulunursa, eklenti güncelleme sırasında bir ses ve bittiğinde bir mesaj çıkaracaktır.  

### Veritabanında videoları arayın:

Eklenti, veritabanına eklenen kanalların videoları arasında anahtar kelimelere göre arama yapabilmemizi sağlar.  

* Varsayılan kısayol olan NVDA+Y ile sanal arayüzü açıyoruz.
* Arama yazma alanını b harfiyle etkinleştiriyoruz.
* Dilediğimiz bir kelime veya cümleyi yazıyoruz.
* enter veya aramayı başlat düğmesine basıyoruz.

Herhangi bir sonuç bulunamazsa, bir mesaj ile bildirilir ve sanal arayüz değiştirilmez.  
Girilen kelime veya cümleye  karşılık gelen videoların bulunması durumunda bir mesaj ile bildirilir ve sonuç arayüzü etkinleştirilir.  
Arama sonuçları arasında gezinmek için yukarı ve aşağı ok tuşları kullanılır.  
Kanal arayüzünde olduğu gibi aynı komutlar mevcuttur; r özel web oynatıcı için tarayıcıda vb. açmak için.  
Kanallar arayüzüne dönebilmek için, Sil tuşuna basarak arama sonuçlarını temizlemek gerekir.  

### Genel arama:

Veritabanı dışında Youtube'ta genel arama yapmak için:

* NVDA+Y ile arayüzü açıyoruz.
* CTRL+B ile arama penceresini etkinleştiriyoruz.
* Dilediğimiz kelime ya da cümleyi yazıyor ve listede kaç adet sonuç görüntüleneceğini seçiyoruz.
* aramayı başlat düğmesine basıyoruz.

Herhangi bir sonuç bulunamazsa, bir mesaj ile bildirilir.  
sonuçlar bulunduğunda yukarı ve aşağı oklarla gezinebileceğimiz ana listeye eklenirler.  
Burada da veritabanı aramasındakiyle aynı kısayollara sahibiz. Tarayıcıda açmak için O, web oynatıcı için r, bağlantıyı kopyalamak için c, vb.  
Veritabanına eklemek istediğiniz herhangi bir kanalda video varsa, bu listedeki n harfine basmak, ad ve url alanları zaten doldurulmuş olan yeni kanal diyaloğunu etkinleştirecektir. İstenirse bu alanlar düzenlenebilir.  
Veritabanındaki aramalarda olduğu gibi, kanal listesine dönmek için, sil tuşuna basmak yeterli olacaktır.  

### arama geçmişi:

Eklenti, son 20 genel aramayı veritabanına kaydeder.  
Geçmişe erişmek için: Genel arama yazma alanındayken, Uygulama veya Shift+F10 tuşlarına basmak yeterli olacaktır.  
Uygulama tuşuna basıldığında açılacak içerik menüsünde, geçmiş arama terimlerimizi alt alta listelenmiş şekilde görebiliyor ve dilediğimiz terimi seçerek yazma alanına eklenmesini sağlayabiliyoruz.

## Çevirmenler:

	Remy Ruiz (Fransızca)
	Angelo Miguel Abrantes (Portekizce)
	Umut KORKMAZ (Türkçe)
	wafiqtaher (Arapça)

