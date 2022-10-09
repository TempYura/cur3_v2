from utils import load_json, add_tag_list, remove_tags_keys


class Manager:
    def __init__(self, posts_file, comments_file, bookmarks_file):
        self.all_posts = load_json(posts_file)
        self.all_comments = load_json(comments_file)
        self.bookmarks = load_json(bookmarks_file)


    def __repr__(self):
        return f"class Manager"


    def get_posts_all(self):
        """возвращает посты"""
        return self.all_posts


    def get_bookmarks(self):
        """возвращает закладки"""
        return self.bookmarks


    def is_user_in_posts(self, user_name):
        """Проверяет наличие имени пользователя в списках создателей постов"""
        user_name = user_name.lower()
        for post in self.all_posts:
            if post['poster_name'].lower() == user_name:
                return True


    def is_user_in_comments(self, user_name):
        """Проверяет наличие имени пользователя в списках создателей комментариев"""
        user_name = user_name.lower()
        for comment in self.all_comments:
            if comment['commenter_name'].lower() == user_name:
                return True


    def get_posts_by_user(self, user_name):
        """возвращает посты определенного пользователя.
        Функция должна вызывать ошибку ValueError если такого пользователя нет
        и пустой список, если у пользователя нет постов."""

        # Проверка наличия имени пользователя
        if not (self.is_user_in_posts(user_name) or self.is_user_in_comments(user_name)):
            raise ValueError(f"Пользователь с именем '{user_name}' не найден")

        requested_posts = [post for post in self.all_posts if user_name.lower() == post['poster_name'].lower()]

        return requested_posts


    def get_post_by_pk(self, pk):
        """Возвращает один пост по его идентификатору"""
        for post in self.all_posts:
            if post['pk'] == pk:
                return post


    def get_post_for_api_by_pk(self, pk):
        """Возвращает один пост по его идентификатору с удаленными живыми тэгами"""
        post = self.get_post_by_pk(pk)
        if post:
            post = remove_tags_keys(post)
            return post
        return None


    def get_all_posts_for_api(self):
        """Возвращает список постов с удаленными живыми тэгами"""
        posts = [remove_tags_keys(post) for post in self.all_posts]
        return posts


    def get_comments_by_post_id(self, post_id):
        """ Возвращает комментарии определенного поста.
        Функция должна вызывать ошибку ValueError если такого поста нет
        и пустой список, если у поста нет комментов. """
        post = self.get_post_by_pk(post_id)

        if not post:
            raise ValueError(f"Нет поста с id = {post_id}")

        requested_comments = [comment for comment in self.all_comments if comment['post_id'] == post_id]
        return requested_comments


    def add_tags_to_all_posts(self):
        """Добавляет параметр со списком тэгов ко всем постам"""
        self.all_posts = [add_tag_list(post) for post in self.all_posts]


    def search_for_posts(self, query):
        """возвращает список постов по ключевому слову"""
        if not query:
            return self.all_posts

        requested_posts = [post for post in self.all_posts if query.lower() in post['content'].lower()]

        return requested_posts


    def get_postids_with_bookmarks(self):
        """Возвращает список postid, которые добавлены в закладки"""
        postids_with_bookmark = [bookmark['post_id'] for bookmark in self.bookmarks]
        return postids_with_bookmark


    def add_bookmark(self, postid):
        """Добавляет пост в закладки"""
        postids_with_bookmark = self.get_postids_with_bookmarks()
        if not postid in postids_with_bookmark:
            new_bookmark = {'post_id': postid,
                            'pk': len(postids_with_bookmark) + 1}
            self.bookmarks.append(new_bookmark)
        return None


    def remove_bookmark(self, postid):
        """Удаляет пост из закладок"""
        postids_with_bookmark = self.get_postids_with_bookmarks()
        for index, pid in enumerate(postids_with_bookmark):
            if postid == pid:
                break
        else:
            return None

        self.bookmarks.pop(index)
        return None


    def get_posts_with_bookmark(self):
        postids_with_bookmark = self.get_postids_with_bookmarks()
        posts_with_bookmark = [self.get_post_by_pk(postid) for postid in postids_with_bookmark]
        return posts_with_bookmark
