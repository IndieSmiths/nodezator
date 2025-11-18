# Translations - How to

Translations are stored in the `.txt` files in this folder.

If you want to contribute translations, all you have to do is add a line with your translation anywhere under a line starting with `en-us`, with the same indentation.

For instance, to add a `pt_br` (Brazilian Portuguese) translation to the text below...

```
continue
    en-us Continue
new_game
    en-us New game
load_game
    en-us Load game
```

...all I had to do was add the translations like so:

```
continue
    en-us Continue
    pt-br Continuar
new_game
    en-us New game
    pt-br Novo jogo
load_game
    en-us Load game
    pt-br Carregar jogo
```

In other words, your line must start with the locale code for the your corresponding language-region combo (just search the web for the locale code for your language/region). For instance, `pt_br` is the locale code for Brazilian Portuguese, in other words, Portuguese (`pt`) as spoken in Brazil (`br`). Then, the locale code must be followed by a space character and the translated text.

Also, don't worry too much about messing up the capitalization/formatting of the locale: you can write `pt-br`, `pt-BR`, `pt_br`, `pt_BR` or really any mix of capitalizations and underscore/hyphen. All of those will be read the same.

You can add translations in any line under the ones starting with `en-us`.

You don't even need to translate everything if you are not sure about the translation of a specific word/sentence. Although we'd appreciate a lot if you provided a full translation for your language/region, as long as you contribute, someone can always come after and finish what you started. Languages missing translations will appear with a `*` near their name/locale code in the options menu, indicating partial support for that language/region.

Although nothing more is required, you may also want to add the name of the language as the natives call it, to make it easier for them to pick it in the options menu. You can add such name in the `.pyl` file within this folder (it is just a text file containing a Python dictionary). If you don't add the name, we'll use the locale code instead in the options menu. In case the language you added is spoken in more than one region, make sure to indicate the region in the name you add. For instance, `English (USA)`, `English (United Kingdom)` or `Português do Brasil`.


## More formatting tips/demonstrations

### Indentation

All indentation must consists of spaces. No tabs or other white space must be used for indentation. Also, the number of spaces used must always be multiples of 4, that is, 0, 4, 8 and so on.

Okay:

```
thank_you
    en-us Thank you
    pt-br Obrigado
```

Not okay:

```
thank_you
  en-us Thank you
  pt-br Obrigado
```

### Translation order

As we said before, you can add translations in any line under the ones starting with `en-us`. The order of the translations below `en-us` doesn't matter, as long as `en-us` is the first (because it is used as the fallback for all languages).

For instance...

```
hello
    en-us Hello
    pt-br Olá
    de-de Hallo
```

...and...

```
hello
    en-us Hello
    de-de Hallo
    pt-br Olá
```

...are okay, as long as `en-us` comes first.


### Comments and empty lines

You can make liberal usage of comments and empty lines in the file if you think it will make the file more readable.

Comments are any lines whose first non-white space character is a `#`.

Example using empty lines and comments:

```

hello

    # there's no need to add punctuation here, as it isn't needed in the context

    en-us Hello

    de-de Hallo
    pt-br Olá
    es-es Hola

```
