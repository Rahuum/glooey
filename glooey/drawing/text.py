#!/usr/bin/env python3

def lorem_ipsum(num_sentences=None, num_paragraphs=None):
    """
    Return the given amount of "Lorem ipsum..." text.
    """
    paragraphs = [
        'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Nam justo sem, malesuada ut ultricies ac, bibendum eu neque. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Aenean at tellus ut velit dignissim tincidunt. Curabitur euismod laoreet orci semper dignissim. Suspendisse potenti. Vivamus sed enim quis dui pulvinar pharetra. Duis condimentum ultricies ipsum, sed ornare leo vestibulum vitae. Sed ut justo massa, varius molestie diam. Sed lacus quam, tempor in dictum sed, posuere et diam. Maecenas tincidunt enim elementum turpis blandit tempus. Nam lectus justo, adipiscing vitae ultricies egestas, porta nec diam. Aenean ac neque tortor. Cras tempus lacus nec leo ultrices suscipit. Etiam sed aliquam tortor. Duis lacus metus, euismod ut viverra sit amet, pulvinar sed urna.',
        'Aenean ut metus in arcu mattis iaculis quis eu nisl. Donec ornare, massa ut vestibulum vestibulum, metus sapien pretium ante, eu vulputate lorem augue vestibulum orci. Donec consequat aliquam sagittis. Sed in tellus pretium tortor hendrerit cursus congue sit amet turpis. Sed neque lacus, lacinia ut consectetur eget, faucibus vitae lacus. Integer eu purus ac purus tempus mollis non sed dui. Vestibulum volutpat erat magna. Etiam nisl eros, eleifend a viverra sed, interdum sollicitudin erat. Integer a orci in dolor suscipit cursus. Maecenas hendrerit neque odio. Nulla orci orci, varius id viverra in, molestie vel lacus. Donec at odio quis augue bibendum lobortis nec ac urna. Ut lacinia hendrerit tortor mattis rhoncus. Proin nunc tortor, congue ac adipiscing sit amet, aliquet in lorem. Nulla blandit tempor arcu, ut tempus quam posuere eu. In magna neque, venenatis nec tincidunt vitae, lobortis eget nulla.',
        'Praesent sit amet nibh turpis, vitae lacinia metus. Ut nisi lacus, feugiat quis feugiat nec, pretium a diam. Aenean bibendum sem eget lorem ullamcorper mattis. Donec elementum purus vel felis vulputate pretium. Duis in ipsum est. Nulla consequat tempor sodales. Donec scelerisque enim eu tellus eleifend imperdiet. Quisque ullamcorper bibendum justo sit amet tincidunt. Donec tempus lacus quis diam varius placerat. Cras metus magna, congue sit amet pulvinar viverra, laoreet vel felis. Praesent sit amet consequat enim. Phasellus arcu nisl, volutpat et molestie a, sagittis a est. Maecenas tincidunt, sem non pharetra mollis, diam nisl ornare tellus, at euismod libero arcu ornare risus. Vestibulum laoreet sollicitudin purus in pharetra. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos.',
        'Nullam pellentesque tempor bibendum. Praesent dictum turpis nec quam consectetur aliquam. Aliquam id turpis nunc. Pellentesque fermentum lacus at tortor auctor venenatis. Maecenas blandit dui lectus. Nunc pellentesque pharetra suscipit. Nullam et metus diam, a congue leo. Curabitur convallis augue in lectus scelerisque non rhoncus lorem molestie. Curabitur in mi a erat dictum pharetra iaculis eu diam.',
        'Nunc lorem magna, rhoncus sodales mattis quis, tincidunt eu mi. In ultrices, lectus ac porttitor tempor, odio nibh facilisis tortor, ac aliquet nisi ante non felis. Praesent ligula nisl, hendrerit ac volutpat non, varius quis tellus. Sed ornare faucibus elit eget faucibus. Nullam sem tellus, commodo id ullamcorper ut, imperdiet ac eros. Sed quis lorem id urna cursus laoreet et eget lacus. Nullam tristique semper sem, eget tempus sem pellentesque sit amet. Donec sed orci augue, convallis tempor tellus. Sed consequat commodo ante a pretium. Nulla et est mauris. Nullam at massa justo. Proin tempor arcu ac eros suscipit varius. Fusce vestibulum quam placerat tellus imperdiet et venenatis diam tristique. Sed pretium tempor tellus, consequat pulvinar massa pellentesque a.',
        'Nulla et lorem vel urna fringilla malesuada ut sit amet tortor. Donec id leo mi. Proin sagittis blandit lacus, placerat imperdiet justo pellentesque ac. Cras iaculis aliquam faucibus. Aenean urna nisi, laoreet ac fringilla dignissim, lacinia eget orci. Vivamus porta lacinia dapibus. Aenean molestie, augue sit amet blandit suscipit, tellus turpis ullamcorper purus, ut pretium turpis lorem quis neque. Pellentesque porta dui at arcu mollis tristique. Suspendisse feugiat felis quis felis sollicitudin porttitor.',
        'Morbi vestibulum, massa quis posuere facilisis, quam lacus porttitor tortor, id fringilla elit velit ac felis. Fusce at luctus risus. Mauris bibendum diam quis odio auctor quis porta massa pellentesque. Proin congue, nisl eu feugiat faucibus, justo orci congue neque, a porta tellus ipsum accumsan turpis. Ut neque enim, dignissim nec fermentum sed, laoreet id orci. Duis fringilla, elit vel tempus porttitor, purus tellus dapibus nisl, eu scelerisque diam lorem vel ante. Ut tempor, urna nec bibendum facilisis, sapien dui ornare lectus, at tempor ligula diam sit amet ligula. Sed a dui in ipsum eleifend egestas.',
        'Quisque ornare fringilla velit, et tincidunt purus convallis vel. Sed venenatis, risus vitae volutpat rhoncus, sapien lorem lacinia elit, id dictum sapien dui vitae lorem. Praesent aliquet accumsan eros quis tempor. Suspendisse eget justo quis arcu bibendum adipiscing. Phasellus quis erat nec massa elementum porta. Nam venenatis elementum mi vel porta. Nunc vel augue non tellus euismod convallis. Curabitur commodo augue vel augue ultrices in fringilla nunc cursus. Mauris auctor laoreet neque, id gravida velit suscipit eget. Maecenas eget libero in lacus auctor feugiat. Pellentesque in lectus felis, eu dictum tortor. Aenean sagittis, massa malesuada dapibus tincidunt, leo massa imperdiet ante, nec mollis nisl turpis in orci. Proin ut purus et eros sagittis volutpat.',
        'Donec molestie sem et metus bibendum convallis semper arcu imperdiet. Curabitur quam libero, fermentum vel adipiscing a, cursus at neque. Maecenas cursus risus vestibulum diam ultricies rutrum. Nullam in enim vel lorem accumsan pulvinar. Cras eget viverra turpis. Sed eget lectus urna, eget venenatis libero. Donec porta libero eu est pulvinar pretium. Ut lectus arcu, aliquam et vestibulum euismod, mattis at orci. Fusce dolor lorem, bibendum a dignissim ut, facilisis eu enim. Morbi erat nibh, interdum non ultricies non, porta ac lacus. Curabitur et nunc nec turpis convallis ullamcorper eget vitae mi.',
        'Curabitur porta molestie sapien, non rhoncus turpis gravida vel. Ut est lacus, elementum eu pretium sit amet, tristique vel orci. Praesent quis suscipit urna. Donec pellentesque molestie tellus sit amet fringilla. Etiam tempus viverra ipsum et tempus. Nunc ut odio imperdiet lorem malesuada bibendum. In aliquam ligula eu sem ullamcorper pulvinar. Quisque sollicitudin placerat dolor et porttitor. Nulla adipiscing lorem id libero aliquet interdum. Suspendisse vehicula fermentum congue. Cras fringilla nisl vitae lectus mollis viverra. Aliquam pharetra lobortis risus, a elementum elit condimentum in. Aenean tincidunt varius faucibus. Nulla non nisi lorem. Suspendisse id sapien a enim lobortis aliquam.',
        'Aliquam erat volutpat. Maecenas neque leo, mattis eu pretium vel, mattis in ante. Nullam sagittis leo diam. Quisque tempor magna in justo vestibulum eget egestas nibh pellentesque. Pellentesque in enim vitae velit pellentesque hendrerit. Cras ultricies, dui et imperdiet gravida, nunc nisl cursus tortor, sit amet porttitor dolor nibh a justo. Praesent ut mauris vitae turpis lobortis scelerisque a nec ligula. Donec turpis erat, iaculis vel dapibus vel, varius id lorem. Integer et enim erat, at eleifend libero.',
        'Phasellus id mi ut nunc cursus pellentesque. Aliquam erat volutpat. Vivamus pretium posuere tellus, ac aliquet metus iaculis eget. Curabitur in mi enim. Duis pretium pretium dui, ut iaculis ipsum scelerisque ut. Proin quam dolor, eleifend et porta vitae, cursus molestie lectus. Aenean dignissim laoreet consectetur. Cras iaculis, lectus imperdiet condimentum suscipit, metus nisi egestas arcu, in tempus sem ipsum eu eros. Vestibulum a orci in elit congue euismod quis quis nisi.',
        'In quis urna leo, at malesuada ipsum. Vestibulum sollicitudin ullamcorper hendrerit. Vestibulum vestibulum mi sodales nulla sagittis commodo. Maecenas nisi lorem, placerat vel aliquet quis, dictum ac ligula. Vestibulum egestas accumsan accumsan. Aenean lobortis pharetra erat convallis pretium. Aliquam consequat facilisis porta. Cras hendrerit nunc et mauris egestas hendrerit. Proin rhoncus, mi id ullamcorper pharetra, ipsum sapien blandit turpis, et ultricies purus neque eget justo. Quisque sodales, nisi in cursus rutrum, elit nibh volutpat lacus, nec sollicitudin erat leo at lectus. Morbi ac dolor mi, vel ultricies quam.',
        'Sed hendrerit nisl id lectus cursus in adipiscing lorem rutrum. Morbi nisl justo, egestas ac aliquet at, scelerisque luctus sapien. Donec sollicitudin elementum mattis. Praesent semper, ante euismod accumsan gravida, ante neque convallis augue, quis vulputate erat nunc vitae tellus. Duis ac lectus ullamcorper purus commodo luctus. Etiam quis augue in purus molestie imperdiet. Lorem ipsum dolor sit amet, consectetur adipiscing elit. Etiam posuere commodo turpis, at pulvinar tortor scelerisque et. Nam vulputate dui sed magna interdum sollicitudin. Nam pulvinar euismod enim vitae malesuada. Aenean non molestie leo. Pellentesque quis lacus mi, et ornare nibh. Etiam pharetra, odio vitae euismod faucibus, nunc urna pulvinar felis, eget molestie est enim sit amet sapien. Vivamus eu neque nulla.',
        'Mauris eget nibh ut augue malesuada tristique nec quis urna. Vestibulum faucibus, mauris sed posuere volutpat, felis lacus vulputate felis, eget luctus lorem nulla sed velit. Proin et purus nec quam tristique cursus. Nullam adipiscing tortor imperdiet purus facilisis eu luctus nulla vestibulum. Sed pulvinar risus sollicitudin risus fringilla et hendrerit lorem accumsan. Vestibulum venenatis est sit amet nunc gravida nec aliquam arcu adipiscing. Nam quis aliquet mauris. Cras nec neque vitae tellus posuere posuere.',
        'Nulla facilisi. Vestibulum sit amet dui turpis. Aliquam erat volutpat. In hac habitasse platea dictumst. Morbi in enim nec massa semper tincidunt. Ut fermentum iaculis dui, sed adipiscing dolor porta at. Nam hendrerit libero non nisi ornare eu cursus mauris accumsan. Ut ullamcorper, odio vel ultrices suscipit, metus libero ornare dui, non dapibus est dui vehicula ipsum.',
        'Nam diam sapien, lacinia vel sollicitudin interdum, faucibus aliquam enim. Mauris tristique iaculis purus eu lacinia. Suspendisse condimentum, dolor a euismod lacinia, leo orci pellentesque orci, non rhoncus turpis lorem sed lacus. Integer velit nisl, rutrum sit amet posuere at, vulputate ultrices tortor. Nullam pharetra, orci tempor dapibus elementum, felis nulla lacinia nunc, quis ultricies dui lectus dictum diam. Praesent eu velit magna, eu lacinia leo. Duis sit amet bibendum dui. Duis tincidunt vulputate dolor eu euismod. Pellentesque nisl sem, mollis ac venenatis a, facilisis vitae ligula. Vivamus sem leo, vestibulum tincidunt iaculis nec, tristique tincidunt mi. Suspendisse imperdiet elit vitae turpis ullamcorper luctus. Aenean in augue mauris. Vivamus nisi libero, dignissim non consectetur sodales, fermentum at sem. Nulla tincidunt fringilla justo quis pulvinar. Nam ac sem sed diam pellentesque egestas vitae ac nisi. Praesent scelerisque dapibus mi vitae tempor.',
        'Donec tempor, massa non pulvinar suscipit, justo dolor pharetra nisl, ut semper libero lorem non tortor. Integer dapibus arcu viverra nisi hendrerit mattis et ut mauris. Maecenas pulvinar, orci vitae ultricies egestas, orci nisi rutrum justo, eu volutpat nibh odio ac purus. Nulla pellentesque sem eget arcu imperdiet ullamcorper. Curabitur nec magna massa. Morbi lobortis urna sed ligula commodo viverra. Pellentesque molestie, ipsum nec faucibus mollis, neque purus sodales sapien, in convallis nisi libero et lorem. Ut sed rutrum leo. Aliquam eleifend, felis quis ullamcorper consequat, dolor mi vulputate ipsum, lobortis ultricies felis nulla at augue.',
        'Ut gravida porttitor arcu, malesuada mollis urna vehicula nec. Suspendisse sagittis nulla condimentum libero lacinia sed dapibus dui egestas. Etiam convallis congue ipsum, eu fermentum turpis rutrum id. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Ut nunc eros, sagittis a venenatis et, interdum in leo. Curabitur urna magna, volutpat in mattis ut, adipiscing et ligula. Nam dignissim mattis accumsan. Nulla vehicula felis vel turpis tempus hendrerit. Phasellus rhoncus vulputate massa, tincidunt euismod dui porttitor ac. Sed ut sapien quam, ac egestas odio. Pellentesque at aliquet ante. Donec rhoncus ornare lacus eu ullamcorper. Vestibulum sit amet hendrerit magna. Nulla sed diam nulla.',
        'Nulla vestibulum sagittis arcu in egestas. Aliquam sed ante justo. Quisque nec dolor nibh, sed feugiat mi. Etiam lorem elit, interdum eu tempor nec, tincidunt eu risus. Fusce id libero augue. Curabitur ultrices, lorem eget mollis fringilla, dolor leo euismod tellus, congue luctus nisi purus vitae urna. Suspendisse tempor orci accumsan sem pretium at accumsan augue tristique. Proin sed turpis at mi feugiat lacinia a nec sem. Suspendisse vel facilisis leo. Class aptent taciti sociosqu ad litora torquent per conubia nostra, per inceptos himenaeos. Duis ornare enim nec ante adipiscing tincidunt. Maecenas ut justo iaculis leo vestibulum blandit quis vitae mauris. Proin in vestibulum massa.',
    ]

    if num_paragraphs:
        paragraphs = paragraphs[:num_paragraphs]

    text = '\n\n'.join(paragraphs)
    sentences = text.split('.')

    if num_sentences:
        sentences = sentences[:num_sentences]

    lorem = '.'.join(sentences).strip()
    if not lorem.endswith('.'):
        lorem += '.'

    return lorem




