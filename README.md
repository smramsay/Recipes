Recipes
=======

Basics
------

Every recipe should start from the format given in `recipe-template.md`.
The filename is the recipe name replacing Unicode characters with their ASCII simplifications.
Technically we're using Pandoc markdown for the tables, but try to stick to basic Markdown syntax.
Look to existing recipes for examples.
Just try to do your best and I can fix it up before merging.
Everything is to be in English, because my German is only slightly better than every other language.

Ingredients
-----------

No table lines are to exceed 114 characters (the width of my Vim terminals side by side).
The ingredient column are just be the name of the ingredient, not how it is prepared.
The amounts in the next column can be either metric, imperial, or mix and match.
Baking is the exception, of course. Everything above a tablespoon or two is to be in grams.
While Unicode is generally accepted, don't use it for fractions; they are hard to read.
The notes column gives how the ingredient is to be prepared, the type of ingredient, or any other short comments.

If there are multiple distinct parts of a dish, feel free to separate them into their own tables.
Add a **bold** heading above each one stating what the part is, i.e. **Sauce** or **Spice Mix**.

The table should be aligned correctly using spaces.
The Python script `markdown-table-format.py` can help with that.

Instructions
------------

Instructions and other lines are **strongly** discouraged from being longer than 114 characters as well.
Instructions should give a single, clear step.
Adding multiple ingredients to a pan at the same time? One step.
Adding an ingredient and cooking before adding the next ingredient? Two steps.

Similar to the ingredients, you can separate distinct parts of the dish into their own instruction lists.

While steps are ideally one line, if you need another just indent it so it matches the numbered line above.
Really try to keep that to a minimum though.
Keep commentary to an absolute minimum as well.

Estimated time for an instruction can be given in parentheses at the end of it, i.e. (3m), (45m - 1h), (30s).
Don't give an overall time for the recipe as that is never correct.
