# Автотесты «Мобильный хоспис»

UI-тесты на Python + Appium + pytest. Отчёт — Allure.

Логин: `login2`  
Пароль: `password2`

## 1. Скопировать проект с GitHub

```
git clone https://github.com/Aluwian/qamid-diplom.git
cd qamid-diplom
```

## 2. Что установить заранее

### Android Studio и SDK

Установить **Android Studio** (вместе с ним ставится Android SDK).

`adb` — программа, которая ставит приложение на эмулятор и показывает список устройств. Она лежит в папке SDK `platform-tools`.

Обычные пути:

- Windows: `C:\Users\Имя\AppData\Local\Android\Sdk\platform-tools`
- Linux: `~/Android/Sdk/platform-tools`

Проверка (подставь свой путь):

```
adb version
```

Если пишет, что команда не найдена — либо каждый раз пиши полный путь к `adb`, либо добавь `platform-tools` в PATH.

**Windows:** Параметры → Система → О программе → Дополнительные параметры системы → Переменные среды → Path → Изменить → Создать → вставить путь к `platform-tools` → ОК. Закрой терминал и открой новый, снова `adb version`.

**Linux:** в конец файла `~/.bashrc` (или `~/.profile`) добавь строку:

```
export PATH="$PATH:$HOME/Android/Sdk/platform-tools"
```

Потом:

```
source ~/.bashrc
adb version
```

### Python 3

Нужен для запуска тестов. Проверка:

```
python3 --version
```

На Windows иногда команда `python`, не `python3`.

### Node.js и Appium Server

Appium ставится через npm, для этого нужен Node.js.

1. Скачать Node.js с сайта [nodejs.org](https://nodejs.org). На сайте есть инструкция для Windows и Linux. Поставь LTS.
2. Установить Appium:

```
npm install -g appium
```

3. Установить драйвер UiAutomator2 (для Android):

```
appium driver install uiautomator2
```

4. Проверка:

```
appium --version
appium driver list --installed
```

5. **Запуск Appium Server** (оставить это окно терминала открытым, пока идут тесты):

```
appium
```

Или явно:

```
appium --address 127.0.0.1 --port 4723
```

Когда сервер готов, в терминале будет что-то вроде:  
`Appium REST http interface listener started on http://127.0.0.1:4723`

Тесты ждут Appium на `127.0.0.1:4723`. Пока сервер не запущен, pytest не подключится к телефону.

### Allure Commandline (для просмотра отчёта)

Нужен, если хочешь открыть HTML-отчёт после прогона. Сам `pytest` без Allure тоже запускается.

## 3. Открыть проект в Android Studio и собрать приложение

1. Android Studio → Open → папка `qamid-diplom`.
2. Дождись Gradle Sync.
3. Если sync падает на AGP 7.0.4 (новая Studio) — правь только у себя, **в git не коммитить**:
   - в корневом `build.gradle`: `classpath 'com.android.tools.build:gradle:7.2.2'`
   - в `gradle/wrapper/gradle-wrapper.properties`: `gradle-7.3.3-bin.zip`
   - снова Sync / Try Again.

Собери приложение — это файл установки (APK), его потом ставят на эмулятор.

Проще всего: зелёный треугольник Run — Studio сама соберёт приложение и поставит на эмулятор. Тогда команда ниже не нужна.

Команда `assembleDebug` нужна только если ставишь через `adb`: `adb` не собирает проект, он ставит уже готовый файл APK. Сначала собери APK из корня проекта:

```
./gradlew assembleDebug
```

На Windows:

```
gradlew.bat assembleDebug
```

Появится файл: `app/build/outputs/apk/debug/app-debug.apk` — его и ставит `adb install`.

## 4. Создать эмулятор

Device Manager → Create Device.

По ТЗ нужно проверить запуск на **API 36**. Основная работа и полный прогон автотестов делались на **API 29** — там suite стабильнее.

### Pixel 6, API 36 (проверка по ТЗ)

- Устройство: Pixel 6  
- Система: API 36 (AVD обычно `Pixel_6_API_36`)  
- Язык после запуска: **русский**  
- Память: RAM **4096 МБ**, VM heap **256 МБ** — для стабильности на длинном прогоне (иначе эмулятор тормозит, тесты чаще падают на старте)  

У образа Google Play кнопка Save в Device Manager часто серая — это нормально.  
Эмулятор выключить. Открыть файл конфигурации AVD (папка `.android/avd/Pixel_6_API_36.avd/config.ini` в домашней директории) и поставить:

```
hw.ramSize=4096
vm.heapSize=256
```

В Studio не путать с «Pixel 6» без API 36 (тот может быть API 31).

### Pixel 4, API 29 (основная работа и полный прогон)

- Устройство: Pixel 4  
- Система: API 29 (AVD обычно `Pixel_4`)  
- Язык: **русский**  
- Память (карандаш у AVD → Show Advanced Settings): RAM **4096 МБ**, VM heap **256 МБ** — тоже для стабильности на длинном прогоне

## 5. Запустить эмулятор и установить приложение

Включить эмулятор кнопкой Play в Device Manager.

Дождись рабочего стола (не надпись «Android is starting»).

```
adb devices
```

Должна быть одна строка `device`.

Поставить приложение через Studio: сверху выбрать `app` и этот эмулятор → зелёный треугольник.  
Если треугольник серый — Sync, выбран `app` и устройство.

Или через `adb` (из корня проекта, APK уже собран):

```
adb install -r -t app/build/outputs/apk/debug/app-debug.apk
```

`-r` — переустановить поверх старой версии, `-t` — разрешить debug-сборку.

На эмуляторе язык **русский**, иначе тесты ищут слова «Логин» и «Новости» и не находят английские подписи.

## 6. Окружение для тестов

Один раз (создать папку с библиотеками):

```
cd tests
python3 -m venv python_venv
source python_venv/bin/activate
pip install -r requirements.txt
```

На Windows активация такая:

```
python_venv\Scripts\activate
```

Перед каждым новым прогоном снова включи окружение.

Из папки `tests/`:

```
cd tests
source python_venv/bin/activate
```

На Windows:

```
cd tests
python_venv\Scripts\activate
```

## 7. Запуск Appium и тестов

Перед тестами:

1. Эмулятор включён, приложение установлено, язык русский.  
2. В **отдельном** терминале запущен Appium:

```
appium
```

### Из папки `tests/` (так удобнее)

```
cd tests
source python_venv/bin/activate
pytest -v
```

### Из корня репозитория

```
source tests/python_venv/bin/activate
PYTHONPATH=tests pytest -v -c tests/pytest.ini tests
```

Один логин (проверка, что среда живая):

```
# из tests/
pytest -v test_login.py::TestLogin::test_valid_authorization
```

```
# из корня
PYTHONPATH=tests pytest -v -c tests/pytest.ini tests/test_login.py::TestLogin::test_valid_authorization
```

Один файл: `pytest -v test_login.py` (из `tests/`)  
Повтор упавших: `pytest -v --lf`

Полный набор на API 36 может идти дольше и чаще ждать загрузки приложения. Если снова сыпется среда — перезапусти Appium и эмулятор, прогони один логин.

## 8. Отчёт Allure

pytest пишет результаты в `tests/allure-results`.

Из `tests/`:

```
allure serve allure-results
```

Из корня:

```
allure serve tests/allure-results
```

## Если тесты упали — сначала среда, не «сломанный поиск»

**pytest пишет ERROR в самом начале теста (setup), ещё до шагов логина.**  
Часто приложение не успело открыться: крутится заставка, эмулятор не догрузился, Appium не запущен, или язык не русский. Тест ищет на экране слово «Новости» (главный экран) или «Логин» — их нет, и падает. Это не значит, что в коде указан неверный id кнопки. Подожди рабочий стол, проверь Appium и язык, запусти один логин ещё раз.

**Сохранение новости прошло, а своей карточки в списке нет.**  
Список после сохранения показывает только первую страницу новостей с общего сервера. Чужие записи и новости «на завтра» занимают место сверху, твоя сегодняшняя `Автотест_…` может не попасть на этот экран. Тест при этом искал правильный заголовок. Свои новости с префиксом `Автотест_` можно удалить руками и прогнать ещё раз. Чужие новости не удалять (так задумано в кейсе 4.2).
