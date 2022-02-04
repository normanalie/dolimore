import requests


class Dolibarr:
    @classmethod
    def config(cls, api_key: str(), url: str()):
        """
        api_key: the dolibarr api_key
        url: the base url of dolibarr installation (http://www.example.com/dolibarr/)
        """
        cls.api_key = api_key
        cls.header = header(cls.api_key)
        cls.base_url = url
        return 0

    @classmethod
    def categories(cls, types: list()) -> list():
        """
        Take the type ["contact", "customer"] and return a list of tuple of all the categories associated with Contacts and/or Customer (Thirdparties)
        Output:
            [(id, label),
             (id, label),
             ...
            ]
        """
        list = []
        for type in types:
            r = requests.get(f"{cls.base_url}/htdocs/api/index.php/categories?sortfield=t.rowid&sortorder=ASC&type={type}", headers=cls.header)
            categories_id = extract_propertie(r.json(), "id")
            categories_label = extract_propertie(r.json(), "label")
            categories = []
            for id, label in zip(categories_id, categories_label):
                categories.append((id, label))
            list.append(categories)

        list = union(list)
        return list

    @classmethod
    def emails(cls, types: list(), categories: list(), operator: str()) -> list():
        """
        Take type of contact (customer and/or contact), categories tags associated (id) and the operator to filter the categories (and/or) 
        Return the list of contact emails
        types: ["customer", "contact"] ; customer is thirdparties
        categories: [int, int, int] ; ids of the categories to look for
        operator: "and" or "or" ; default or, how the filter work between categories, "and" is intersection and "or" is union
        """
        emails = get_all_emails(cls.base_url, cls.header, types, categories)
        if operator == "and":
            emails = intersection(emails)
        else:
            emails = union(emails)
        return emails

    #TODO: Separate in two functions, one to get customers IDs and one to get contacts from cust ID
    @classmethod
    def customer_contacts_from_cat(cls, categories: list(), operator: str()) -> list():
        """
        Take a list of customer categories and the operator to filter the categories (and/or).
        Return the contact emails associated with.
        """
        customer_ids = []
        emails = []
        for categorie in categories:
            r = requests.get(f"{cls.base_url}/htdocs/api/index.php/categories/{categorie}/objects?type=customer", headers=cls.header)
            id = extract_propertie(r.json(), "id")
            customer_ids.append(id)

        if operator == "and":
            customer_ids = intersection(customer_ids)
        else:
            customer_ids = union(customer_ids)
        
        customer_ids = ','.join(customer_ids)  # Dolibarr API can take a comma-separated list of ids to reduce API calls 
        r = requests.get(f"{cls.base_url}/htdocs/api/index.php/contacts?thirdparty_ids={customer_ids}", headers=cls.header)
        emails.extend(extract_propertie(r.json(), "email"))

        emails = cls.delete_duplicates(emails)
        return emails

    @classmethod
    def delete_duplicates(cls, lst: list()) -> list():
        """
        Take a list or a list of lists and return the same list without the duplicated elements
        """
        try:  # A single list 
           return list(dict.fromkeys(lst)) # Convert to dict then back to list. In fact, a dict couldn't have two times the same key.
        except TypeError:  # A list of lists
            seen_items = []
            for ls in lst[:]: # Iterate over a copy because we remove item so the lenght of the list decrease -> if we remove in the original, some items will be skip
                for elem in ls[:]:  
                    print(elem)
                    print(elem in seen_items)
                    if elem in seen_items:
                        ls.remove(elem)
                    else:
                        seen_items.append(elem)
                if ls == []:
                    lst.remove(ls)
            return lst


    


def header(api_key):
    return {"DOLAPIKEY": api_key}


def extract_propertie(objects: list(), propertie: str()) -> list():
    """
    Take a json objects list: [{objectA}, {objectB}, ...] and the propertie to extract
    Return a list of the giver propertie of each object: [objectA[propertie], objectB[propertie], ...]
    """
    list = []
    for object in objects:
        if object[propertie] and object[propertie] != "None":
            list.append(object[propertie])
    return list


def get_all_emails(base_url, header, types: list(), categories: list()): 
    emails = []
    for type in types:
        for categorie in categories:
            r = requests.get(f"{base_url}/htdocs/api/index.php/categories/{categorie}/objects?type={type}", headers=header)
            emails.append(extract_propertie(r.json(), "email"))
    return emails


def union(lst: list()) -> list():
    """
    Take a list of lists and return the union ("sum") of them
    [["a", "b", "c"], ["c", "d", "e"]] -> ["a", "b", "c", "d", "e"]
    """
    union = []
    for lists in lst:
        union.extend(lists)  # extend is like append but add the elements one by one, not the entire list() object
    union = Dolibarr.delete_duplicates(union)
    return union


def intersection(lst: list()) -> list():
    """
    Take a list of lists and return the intersection (common elements in each lists)
    [["a", "b", "c"], ["c", "d", "e"]] -> ["c"]

    Something INTER Nothing = Something
    [["a", "b", "c"], []] -> ["a", "b", "c"]
    """
    try: # [["a", "b", "c"], []] -> ["a", "b", "c"]
        intersection = lst[0]
    except IndexError:
        intersection = []

    precedent_list = None
    for lists in lst:
        if precedent_list:
            intersection = [elem for elem in lists if elem in precedent_list]
        precedent_list = lists

    return intersection 
