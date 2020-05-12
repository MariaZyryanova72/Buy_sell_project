## Скачивание репозитория:

    Перейдите в директорию, в которую будите клонировать. Откройте консоль или Git Bach Here.
	Затем введите команду 
	git clone https://github.com/MariaZyryanova72/Buy_sell_project(Для windows), 
	sudo git clone https://github.com/MariaZyryanova72/Buy_sell_project(Для linux).


## Руководство по настройке:

1. Если у вас не установлен Docker и Docker-compose, то вам необходимо их установить.
	Ссылки для скачивания, инструкция по установке:
	+ https://www.digitalocean.com/community/tutorials/docker-ubuntu-18-04-1-ru
	+ https://www.digitalocean.com/community/tutorials/how-to-install-docker-compose-on-ubuntu-18-04-ru
2. После установки вам необходимо перейти в папу Buy_sell_project. 
3. Создаем образы и запускаем контейнеры:
	
		+  sudo docker-compose up -d						смонтировать и запустить
		
4. Переходим на сайт по адресу - http://84.201.173.242 или http://stend72.ru



## Использование:


    Сайт Купи-продай был написан для защиты проекта в Яндекс лицее. 
    Целью сайта является размещение объявление для продажи и покупка товаров других пользователей. 
	
	
 ####1. Для размещения объявления необходимо зарегистрироваться на сайте.

![alt text](readme_img/1.jpg)

после регистрации пройдите авторизацию

![alt text](readme_img/2.jpg)
        
Теперь вы можете размещать собственные объявления, но необходимо перейти в Личные объявления

![alt text](readme_img/3.jpg)

![alt text](readme_img/4.jpg)
Собственные объявления вы можете редактировать и удалять в разделе Личные объявления

![alt text](readme_img/5.jpg)
        
Так и на главной странице товара

![alt text](readme_img/6.jpg)
	
####2. На главной странице вы можете увидеть объявления других пользователей.
		
Чтобы узнать больше о товаре, который вам понравился, просто нажмите на объявление, вы попадете на гланую страницу товара.
    
![alt text](readme_img/7.jpg)

Искать товары вы можете, вводя в поисковую строку ключевые слова.
    
![alt text](readme_img/8.jpg)
 
![alt text](readme_img/9.jpg)
    
Или переключать на панели справа категории, поиск выдаст вам все товары, принадлежащие этой категории.

![alt text](readme_img/10.jpg)

![alt text](readme_img/11.jpg)
 
####3. Навык Алисы (Алиса пока не прошла модерацию)
Также вы можете искать необходимый вам товар через Алису. Мной написан навык по поиску товаров на сайте купи-продай.

Когда Алиса вас спросит - "Что вы хотите? Купить или продать?". Просто ответьте - "Купить".
И вводите название товара или ключевое слово, Алиса вам отправит фотографию с кратким
 описание товара. Если же вы захотите узнать больше о товаре, то просто нажмите на ссылку - " Узнать больше"
 
В настройках Алисы вы можете указать адрес https://www.dekor72.ru/alice/talk
Или при развертывании своего проекта указать адрес домена там, где разверываете Алису. 

![alt text](readme_img/12.jpg)

![alt text](readme_img/13.jpg)
	
![alt text](readme_img/14.jpg)
	
Команда "Продать" сейчас находится в разработке.
 
_________________________________

P.s. Надеюсь у вас все работает =)
Работу выполнела Зырянова Мария 
	+ vk - https://vk.com/mariyazz