class PhotoSort:
    priorities = {'q': 0, 'r': 1, 'p': 2, 'o': 3, 'm': 4, 's': 5}

    @staticmethod
    def sort_photos_by_type(photos: list):
        for item in photos:
            if item[1] in PhotoSort.priorities:
                item[1] = PhotoSort.priorities[item[1]]
        return list(sorted(photos, key=lambda photo_list: photo_list[1]))


def filter_photos_by_size(photos: list, photo_count: int, excluded_types: tuple=('x', 'y', 'z', 'w')):
    ''' Собирает из постов по одному изображению одного из типов размеров, которые указаны в параметре needed_types. '''
    filtered_photos = ''
    urls_without_params = set()
    allitems = []
    for photo_dict in photos:
        for photo in photo_dict:
            if photo['type'] not in excluded_types:
                allitems.append(
                            [photo['url'], photo['type']]
                                )
                urls_without_params.add(photo['url'][:50])
            allitems = PhotoSort.sort_photos_by_type(allitems)
    if len(urls_without_params) == 0:
        filtered_photos = '<no_images>'
    elif len(urls_without_params) == 1:
        filtered_photos = allitems[0][0]
    else:
        unique_photo_urls = []
        for index, item in enumerate(allitems):
            if index < photo_count:  # Первые photo_count-1 фото - это фото с наиболее подходящим для отображения разрешением.
                if photo_count in range(4, 7):
                    PhotoSort.priorities = {'m': 0, 'p': 1, 'o': 2, 's': 3, 'q': 4, 'r': 5}
                elif photo_count in range(7, 11):
                    PhotoSort.priorities = {'o': 0, 's': 1, 'm': 2, 'p': 3, 'q': 4, 'r': 5}
                else:
                    PhotoSort.priorities = {'q': 0, 'r': 1, 'p': 2, 'o': 3, 'm': 4, 's': 5}
                allitems = PhotoSort.sort_photos_by_type(allitems)
                unique_photo_urls.append(item[0])
            else:
                break
        for photo_url in unique_photo_urls:
            filtered_photos += photo_url + '\n'
            # TODO: исправить баг: При отображении постов с 2+ изображений, которые находятся после поста с copy_history (перепост), фото из предыдущего поста отображаются на следующем.
    return filtered_photos.rstrip()


def get_filtered_post_photos(photo_list: list, photo_counter: list, post_number: int, final_photo_refs_list: list):
    post_photos_with_sizes = [item['photo']['sizes'] for item in photo_list]
    photo_count = len(photo_list)
    photo_counter[post_number] = photo_count
    refs = filter_photos_by_size(photos=post_photos_with_sizes, photo_count=photo_count)
    final_photo_refs_list.append(refs)
    a = 0

