animal = """Black,
White,
Brown,
Brown Tabby,
Tan,
Blue,
Orange Tabby,
Red,
Brown Brindle,
Tricolor,
Blue Tabby,
Tortie,
Calico,
Gray,
Chocolate,
Torbie,
Cream Tabby,
Sable,
Cream,
Fawn,
Yellow,
Buff,
Lynx Point,
Blue Merle,
Seal Point,
Black Brindle,
Gray Tabby,
Black Tabby,
Flame Point,
Orange,
Brown Merle,
Black Smoke,
Gold,
Tortie Point,
Silver,
Red Tick,
Blue Tick,
Blue Point,
Lilac Point,
Silver Tabby,
Yellow Brindle,
Red Merle,
Apricot,
Calico Point,
Blue Cream,
Blue Tiger,
Chocolate Point,
Green,
Pink,
Blue Smoke,
Brown Tiger,
Agouti,
Silver Lynx Point,
Liver,
Liver Tick,
Black Tiger"""

spliter = animal.split(',\n')

for idx, thing in enumerate(spliter):
    print(f'"{thing}"' + " : " + str(idx+1) + ',')
