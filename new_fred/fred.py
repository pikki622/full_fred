
from .tags import Tags

# expand on current docstrings to explain with greater clarity
# define tags, sources, series, categories, releases, etc.
# define realtime_start and realtime_end
# create a thing on how to set environment variables to enable broad use 
# integrate ALFRED, GeoFRED

# go heavy on examples
# make keys for each stack the parameters that were passed, not only the id used
# set default params to None, not fred web service params
# add option to retrieve tag notes
# heavily integrate pandas
# add parameter to return all requested data as dataframes
# create a stack that holds only the parameters of the *latest* request
# must provide for case where new parameters are sent to already-used method and data has to be queried again
# Can save metadata about last df query to check new request against
class Fred(Tags):
    """
    Clarify what series_stack is
    FRED tags are attributes assigned to series
    """

    # go ham on docstrings for methods
    """
    Use api_key_found() to determine if an api key is found as 
    an environment variable with name FRED_API_KEY
    """
    
    def __init__(self):
        super().__init__()
        self.unit_info = dict() # put explanation of units options<- no, explain in method doc
#        self.category_stack = dict() # eh
#        self.release_stack = dict()
#        self.series_stack = dict() # eh
#        self.source_stack = dict()
#        self.tag_stack = dict()

    # not finished
    # may be redundant
    def peek_last_category_query(self):
        """
        Returns the key (method called + category_id used) 
        of the top of the category query stack
        """
        return self.category_stack.keys() # fix this

    def get_all_category_query_keys(self):
        """
        Returns the keys (key: str = method called + category_id used) 
        of all queries in the category query stack
        """
        return list(self.category_stack.keys())

    # work on this
    def get_category_query(self, key: str):
        """
        Returns the value for key from the category query stack 
        (key: str = method called + category_id used) 
        of all queries in the category query stack

        Parameters
        ----------

        Returns
        -------

        """
        try:
            query = self.category_stack[key]
        except KeyError:
            print("Key %s " % key)
        return self.category_stack.keys() # fix this

    # fred/category

    def get_a_category(self, category_id: int) -> dict:
        """
        Get a category of FRED data using its id

        Parameters
        ----------

        Returns
        -------

        Notes
        -----
        fred/category
        """
        try:
            url_prefix = "category?category_id=" + str(category_id)
        except TypeError:
            print("Cannot cast category_id %s to str" % category_id)
        json_data = self._fetch_data(url_prefix)
        key = "get_a_category__category_id_" + str(category_id)
        self.category_stack[key] = json_data
        return json_data

    def get_child_categories(
            self, 
            category_id: int,
            realtime_start: str = None,
            realtime_end: str = None,
            ) -> dict:
        """
        Get child categories (category_id, name, parent_id) 
        of category associated with category_id

        Parameters
        ----------

        Returns
        -------

        Notes
        -----
        fred/category/children
        """
        url_prefix = "category/children?category_id=" 
        try:
            url_prefix += str(category_id)
        except TypeError:
            print("Cannot cast category_id %s to str" % category_id)
        realtime_period = self._get_realtime_date(
                realtime_start, 
                realtime_end
                )
        url_prefix += realtime_period
        json_data = self._fetch_data(url_prefix)
        key = "get_child_categories__category_id_" + str(category_id)
        self.category_stack[key] = json_data
        return json_data

    # add option for tag notes
    def get_related_categories(
            self, 
            category_id: int,
            realtime_start: str = None, 
            realtime_end: str = None,
            ):
        """
        Get the related categories for a category. 
        add all parameters fred offers
        unclear how to test rn
        count parameter***

        Parameters
        ----------
        category_id: int
            the id of the category
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred

        Returns 
        -------

        Notes
        -----
        fred/category/related
        """
        url_prefix = "category/related?category_id="
        try:
            url_prefix += str(category_id)
        except TypeError:
            print("Cannot cast category_id %s to str" % category_id) # doesn't this line contradict itself?
        # add realtime params to key if they're passed (later)
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
            }
        url = self._add_optional_params(url_prefix, optional_args)
        self.category_stack[category_id] = self._fetch_data(url)
        return self.category_stack[category_id]

    # add parameter to remove discontinued series
    def get_series_in_a_category(
            self, 
            category_id: int,
            realtime_start: str = None,
            realtime_end: str = None,
            limit: int = None,
            offset: int = None,
            order_by: str = None,
            sort_order: str = None,
            filter_variable: str = None,
            filter_value:str = None,
            tag_names: list = None,
            exclude_tag_names: list = None,
            ): 
        """
        Get the series that belong to a category (metadata, not dataframes for each series). 
        add all parameters fred offers
        unclear how to test rn
        count parameter***

        Parameters
        ----------
        category_id: int
            the id of the category
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred
        limit: int default None
        offset: int default None
        order_by: str default None
        sort_order: str default None
        filter_variable: str default None
        filter_value: str default None
        tag_names: list default None
        exclude_tag_names: list default None

        Returns 
        -------

        Notes
        -----
        fred/category/series
        """
        url_prefix = "category/series?category_id="
        try:
            url_prefix += str(category_id)
        except TypeError:
            print("Cannot cast category_id %s to str" % category_id) # doesn't this line contradict itself?
        # add realtime params to key if they're passed (later)
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                "&limit=": limit,
                "&offset=": offset,
                "&order_by=": order_by,
                "&sort_order=": sort_order,
                "&filter_variable=": filter_variable,
                "&filter_value=": filter_value,
                "&tag_names=": tag_names,
                "&exclude_tag_names=": exclude_tag_names,
            }
        url = self._add_optional_params(url_prefix, optional_args)
        self.category_stack[category_id] = self._fetch_data(url)
        return self.category_stack[category_id]

    def get_tags_for_a_category(
            self, 
            category_id: int,
            realtime_start: str = None,
            realtime_end: str = None,
            tag_names: list = None,
            tag_group_id: str = None,
            search_text: str = None,
            limit: int = None,
            offset: int = None,
            order_by: str = None,
            sort_order: str = None,
            ):
        """
        Get the FRED tags for a category.
        add all parameters fred offers
        unclear how to test rn
        count parameter***

        Parameters
        ----------
        category_id: int
            the id of the category
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred
        tag_names: list default None
        tag_group_id: list default None
        limit: int default None
        offset: int default None
        order_by: str default None
        sort_order: str default None

        Returns 
        -------

        Notes
        -----
        fred/category/tags
        """
        url_prefix = "category/tags?category_id="
        try:
            url_prefix += str(category_id)
        except TypeError:
            print("Cannot cast category_id %s to str" % category_id) # doesn't this line contradict itself?
        # add realtime params to key if they're passed (later)
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                "&tag_names=": tag_names,
                "&tag_group_id=": tag_group_id,
                "&search_text=": search_text,
                "&limit=": limit,
                "&offset=": offset,
                "&order_by=": order_by,
                "&sort_order=": sort_order,
            }
        url = self._add_optional_params(url_prefix, optional_args)
        self.category_stack[category_id] = self._fetch_data(url)
        return self.category_stack[category_id]

    def get_related_tags_for_a_category(
            self, 
            category_id: int,
            tag_names: list,
            realtime_start: str = None,
            realtime_end: str = None,
            exclude_tag_names: list = None,
            tag_group_id: str = None,
            search_text: str = None,
            limit: int = None,
            offset: int = None,
            order_by: str = None,
            sort_order: str = None,
            ):
        """
        Get the related FRED tags for one or more FRED tags within a category.
        add all parameters fred offers
        unclear how to test rn
        count parameter***

        Parameters
        ----------
        category_id: int
            the id of the category
        tag_names: list 

        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred

        tag_group_id: list default None
        search_text: str, default None
        limit: int default None
        offset: int default None
        order_by: str default None
        sort_order: str default None

        Returns 
        -------

        Notes
        -----
        fred/category/related_tags
        """
        url_prefix = "category/related_tags?category_id="
        try:
            url_prefix += str(category_id)
        except TypeError:
            print("Cannot cast category_id %s to str" % category_id) # doesn't this line contradict itself?
        url_prefix += "&tag_names="
        try:
            url_prefix += ";".join(tag_names)
        except TypeError:
            print("tag_names must be list or tuple")
        # add realtime params to key if they're passed (later)
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                "&exclude_tag_names=": exclude_tag_names,
                "&tag_group_id=": tag_group_id,
                "&search_text=": search_text,
                "&limit=": limit,
                "&offset=": offset,
                "&order_by=": order_by,
                "&sort_order=": sort_order,
            }
        url = self._add_optional_params(url_prefix, optional_args)
        self.category_stack[category_id] = self._fetch_data(url)
        return self.category_stack[category_id]

    # fred/release 

    def get_all_releases(
            self,
            realtime_start: str = None, 
            realtime_end: str = None,
            limit: int = None,
            offset: int = None,
            order_by: str = None,
            sort_order: str = None,
            ) -> dict:
        """
        Get all releases of economic data.

        Parameters
        ----------
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred
        limit: int default None
        offset: int default None
        order_by: str default None
        sort_order: str default None

        Returns 
        -------
        dict

        Notes
        -----
        fred/releases
        """
        url_prefix = "releases?"
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                "&limit=": limit,
                "&offset=": offset,
                "&order_by=": order_by,
                "&sort_order=": sort_order,
            }
        url = self._add_optional_params(url_prefix, optional_args)
        # change key (first part of key) to all_releases?
        self.release_stack["releases"] = self._fetch_data(url)
        return self.release_stack["releases"]

    def get_release_dates_all_releases(
            self,
            realtime_start: str = None, 
            realtime_end: str = None,
            limit: int = None,
            offset: int = None,
            order_by: str = None,
            sort_order: str = None,
            include_release_dates_with_no_data: bool = None,
            ) -> dict:
        """
        Get release dates for all releases of economic data.

        Parameters
        ----------
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred
        limit: int default None
        offset: int default None
        order_by: str default None
        sort_order: str default None
        include_release_dates_with_no_data: bool, default None

        Returns 
        -------
        dict

        Notes
        -----
        fred/releases
        """
        url_prefix = "releases/dates?"
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                "&limit=": limit,
                "&offset=": offset,
                "&order_by=": order_by,
                "&sort_order=": sort_order,
                "&include_release_dates_with_no_data":
                include_release_dates_with_no_data,
            }
        url = self._add_optional_params(url_prefix, optional_args)
        self.release_stack["dates_all_releases"] = self._fetch_data(url)
        return self.release_stack["dates_all_releases"]





    def get_a_release(
            self,
            release_id: int,
            realtime_start: str = None, 
            realtime_end: str = None,
            ):
        """
        Get a release of economic data
        
        Parameters
        ----------
        release_id: int
            id for a release
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred

        Returns 
        -------

        Notes
        -----
        fred/release
        """
        url_prefix = "release?release_id="
        try:
            url_prefix += str(release_id)
        except TypeError:
            print("Unable to cast release_id %s to str" % release_id)
        realtime_period = self._get_realtime_date(
                realtime_start, 
                realtime_end
                )
        url_prefix += realtime_period
#        breakpoint()
        self.release_stack[release_id] = self._fetch_data(url_prefix)
        return self.release_stack[release_id]

    def get_release_dates(
            self,
            release_id: int,
            realtime_start: str = None,
            realtime_end: str = None,
            limit: int = None,
            offset: int = None,
            sort_order: str = None,
            include_release_dates_with_no_data: bool = None,
            ) -> dict:
        """
        Get release dates for a release of economic data.

        Parameters
        ----------
        release_id: int
            id for a release
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred
        include_release_dates_with_no_data: bool default False
            if None, FRED excudes release dates that don't have data, 
            notably future dates that are already in FRED's calendar

        Returns 
        -------

        Notes
        -----
        fred/release/dates
        """
        url_prefix = "release/dates?release_id="
        try:
            url_prefix += str(release_id)
        except TypeError:
            print("Unable to cast release_id %s to str" % release_id)
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                "&limit=": limit,
                "&offset=": offset,
                "&sort_order=": sort_order,
                "&include_release_dates_with_no_data=": 
                include_release_dates_with_no_data,
            }
        url = self._add_optional_params(url_prefix, optional_args)
        self.release_stack[release_id] = self._fetch_data(url)
        return self.release_stack[release_id]

    def get_series_on_a_release(
            self,
            release_id: int,
            realtime_start: str = None,
            realtime_end: str = None,
            limit: int = None,
            offset: int = None,
            order_by: str = None,
            sort_order: str = None,
            filter_variable: str = None,
            filter_value:str = None,
            tag_names: list = None,
            exclude_tag_names: list = None,
            ) -> dict:
        """
        Get release dates for a release of economic data.

        Parameters
        ----------
        release_id: int
            id for a release
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred
        limit: int, default None (FRED will use limit = 1_000)
            maximum number of results to return
            range [1, 1_000]
        offset: non-negative integer, default None (offset of 0)
        order_by: str, default "series_count"
            order results by values of the specified attribute
            can be one of "series_count", "popularity", "created", "name", "group_id"
        sort_order: str, default None (FRED will use "asc")
            sort results in ascending or descending order for attribute values specified by order_by
        filter_variable: str = None,
        filter_value:str = None,
        tag_names: list
            list of tags (str); each tag must be present in the tag of returned series
            example: ['defense', 'investment']
        exclude_tag_names: list, default None (don't exclude any tags)

        Returns 
        -------
        dict

        Examples
        -----

        Notes
        -----
        fred/release/series
        """
        url_prefix_params = dict(
                a_url_prefix = "release/series?release_id=",
                an_int_id = release_id)
        url_prefix = self._append_id_to_url(**url_prefix_params)
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                "&limit=": limit,
                "&offset=": offset,
                "&order_by=": order_by,
                "&sort_order=": sort_order,
                "&filter_variable=": filter_variable,
                "&filter_value=": filter_value,
                "&tag_names=": tag_names,
                "&exclude_tag_names=": exclude_tag_names,
                }
        url = self._add_optional_params(url_prefix, optional_args)
        self.release_stack[release_id] = self._fetch_data(url)
        return self.release_stack[release_id]

    def get_sources_for_a_release(
            self,
            release_id: int,
            realtime_start: str = None,
            realtime_end: str = None,
            ) -> dict:
        """
        Get the sources for a release of economic data.

        Parameters
        ----------
        release_id: int
            id for a release
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred

        Returns 
        -------
        dict

        Examples
        -----

        Notes
        -----
        fred/release/sources
        """
        url_prefix_params = dict(
                a_url_prefix = "release/sources?release_id=",
                an_int_id = release_id)
        url_prefix = self._append_id_to_url(**url_prefix_params)
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                }
        url = self._add_optional_params(url_prefix, optional_args)
        self.release_stack[release_id] = self._fetch_data(url)
        return self.release_stack[release_id]

    def get_tags_for_a_release(
            self,
            release_id: int,
            realtime_start: str = None,
            realtime_end: str = None,
            tag_names: list = None,
            tag_group_id: str = None,
            search_text: str = None,
            limit: int = None,
            offset: int = None,
            order_by: str = None,
            sort_order: str = None,
            ) -> dict:
        """
        Get the FRED tags for a release

        Parameters
        ----------
        release_id: int
            id for a release
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred
        tag_names: list
            list of tags (str); each tag must be present in the tag of returned series
            example: ['defense', 'investment']
        tag_group_id: str, default None
            a tag group id to filter tags by type with
            can be one of 'freq' for frequency, 'gen' for general or concept, 
            'geo' for geography, 'geot' for geography type, 'rls' for release, 
            'seas' for seasonal adjustment, 'src' for source
        search_text: str, default None
            the words to find matching tags with
            if None, no filtering by search words
        limit: int, default None (FRED will use limit = 1_000)
            maximum number of results to return
            range [1, 1_000]
        offset: non-negative integer, default None (offset of 0)
        order_by: str, default "series_count"
            order results by values of the specified attribute
            can be one of "series_count", "popularity", "created", "name", "group_id"
        sort_order: str, default None (FRED will use "asc")
            sort results in ascending or descending order for attribute values specified by order_by

        Returns 
        -------
        dict

        Examples
        -----

        Notes
        -----
        fred/release/tags
        """
        url_prefix = "release/tags?release_id="
        try:
            url_prefix += str(release_id)
        except TypeError:
            print("Unable to cast release_id %s to str" % release_id)
        # method to try to join string by join_string for "&tag_names="
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                "&tag_group_id=": tag_group_id,
                "&search_text=": search_text,
                "&limit=": limit,
                "&offset=": offset,
                "&order_by=": order_by,
                "&sort_order=": sort_order,
                }
        url = self._add_optional_params(url_prefix, optional_args)
        self.release_stack[release_id] = self._fetch_data(url)
        return self.release_stack[release_id]

    def get_related_tags_for_release(
            self,
            release_id: int,
            tag_names: list,
            realtime_start: str = None,
            realtime_end: str = None,
            exclude_tag_names: list = None,
            tag_group_id: str = None,
            search_text: str = None,
            limit: int = None,
            offset: int = None,
            order_by: str = None,
            sort_order: str = None,
            ) -> dict:
        """
        Get the related FRED tags for one or more FRED tags within a release.

        Parameters
        ----------
        release_id: int
            id for a release
        tag_names: list
            list of tags (str); each tag must be present in the tag of returned series
            example: ['defense', 'investment']
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred
        exclude_tag_names: list, default None (don't exclude any tags)
            tags that returned series must not have
        tag_group_id: str, default None
            a tag group id to filter tags by type with
            can be one of 'freq' for frequency, 'gen' for general or concept, 
            'geo' for geography, 'geot' for geography type, 'rls' for release, 
            'seas' for seasonal adjustment, 'src' for source
        search_text: str, default None
            the words to find matching tags with
            if None, no filtering by search words
        limit: int, default None (FRED will use limit = 1_000)
            maximum number of results to return
            range [1, 1_000]
        offset: non-negative integer, default None (offset of 0)
        order_by: str, default "series_count"
            order results by values of the specified attribute
            can be one of "series_count", "popularity", "created", "name", "group_id"
        sort_order: str, default None (FRED will use "asc")
            sort results in ascending or descending order for attribute values specified by order_by

        Returns 
        -------
        dict

        Examples
        -----

        Notes
        -----
        fred/release/related_tags
        """
        url_prefix = "release/related_tags?release_id="
        try:
            url_prefix += str(release_id)
        except TypeError:
            print("Unable to cast release_id %s to str" % release_id)
        url_prefix += "&tag_names="
        try:
            url_prefix += ";".join(tag_names)
        except TypeError:
            print("tag_names must be list or tuple")
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                "&exclude_tag_names=": exclude_tag_names,
                "&tag_group_id=": tag_group_id,
                "&search_text=": search_text,
                "&limit=": limit,
                "&offset=": offset,
                "&order_by=": order_by,
                "&sort_order=": sort_order,
                }
        url = self._add_optional_params(url_prefix, optional_args)
        self.release_stack[release_id] = self._fetch_data(url)
        return self.release_stack[release_id]

    def get_release_tables(
            self,
            release_id: int,
            element_id: int = None,
            include_observation_values: bool = None,
            observation_date: str = None,
            ):
        """
        Get a release of economic data
        *add fred's description*
        
        Parameters
        ----------
        release_id: int
            id for a release
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred
        include_observation_values: bool default False
        observation_date: str, default None
            the observation date to be included with the returned release table

        Returns 
        -------

        Notes
        -----
        fred/release/tables
        """
        url_prefix = "release?release_id="
        try:
            url_prefix += str(release_id)
        except TypeError:
            print("Unable to cast release_id %s to str" % release_id)
        url_base = [self._FredBase__url_base, url_prefix, "&api_key=",]
#        breakpoint()
        base = "".join(url_base)
        file_type = "&file_type=json"
        if element_id is not None:
            str_element_id = "&element_id=" + str(element_id)
        if self._FredBase__api_key_env_var:
            if element_id is None:
                json_data = self._get_response(base + os.environ["FRED_API_KEY"] + file_type)
            else:
                json_data = self._get_response(base + os.environ["FRED_API_KEY"] + str_element_id + file_type)
        else:
            json_data = self._get_response(base + self.__api_key + file_type)
        if json_data is None:
            message = "Data could not be retrieved using" \
                    "id : %s" % an_id
            print(message)
            return
        self.release_stack[release_id] = self._fetch_data(url_prefix)
        return self.release_stack[release_id] 

    # fred/series

    def get_series(
            self, 
            series_id: str, 
            realtime_start: str = None, 
            realtime_end: str = None,
            ):
        """
        Get an economic data series using series_id. If the 
        series hasn't been fetched it's added to Fred.series_stack, 
        a dictionary that stores FredSeries objects 
        all parameters fred offers: y (need tags though)
        FRED accepts upper case series_id: maybe integrate something to capitalize automatically
        default realtime start and realtime end: first to last available
        if series_id attribute is not set, FredSeries.series_id will be set to 
        the series_id passed in this method
        explain that not merely the requested data is retrieved and stored but rather
        a FredSeries object is instantiated 

        Parameters
        ----------
        series_id: int
            the id of the series
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred

        Returns
        -------

        Notes
        -----
        fred/series
        """
        if not series_id in self.series_stack.keys():
            self.series_stack[series_id] = FredSeries(series_id)
        params = dict(
                series_id = series_id, # revisit: series_id given in constructor above
                                        # but above code may not be executed
                realtime_start = realtime_start,
                realtime_end = realtime_end,
                )
        return self.series_stack[series_id].get_series(**params) 

    def get_categories_of_series(
            self,
            series_id: str, 
            realtime_start: str = None, 
            realtime_end: str = None,
            ):
        """
        Get the categories that FRED uses to classify series associated with series_id
        if series_id attribute is not set, FredSeries.series_id will be set to 
        the series_id passed in this method
        add examples
        explain that not merely the requested data is retrieved and stored but rather
        a FredSeries object is instantiated so the data need not be requested again: it's stored
        (but deletable to minimize risk of bloat)
        all parameters fred offers: y (need tags though)

        Parameters
        ----------
        series_id: int
            the id of the series
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred

        Returns
        -------

        Notes
        -----
        fred/series/categories
        """
        if not series_id in self.series_stack.keys():
            self.series_stack[series_id] = FredSeries(series_id)
        params = dict(
                series_id = series_id, # revisit: series_id given in constructor above
                                        # but above code may not be executed
                realtime_start = realtime_start,
                realtime_end = realtime_end,
                )
        return self.series_stack[series_id].get_categories_of_series(**params) 

    def get_series_df(
            self, 
            series_id: str,
            realtime_start: str = None, 
            realtime_end: str = None,
            limit: int = 100_000,
            offset: int = 0,
            sort_order: str = 'asc',
            observation_start: str = "1776-07-04",
            observation_end: str = "9999-12-31",
            units: str = None,
            frequency: str = None,
            aggregation_method: str = None,
            output_type: int = None,
            vintage_dates: str = None,
            ):
        """
        Get the data values in (pandas) DataFrame form for series associated
        with series_id
        distinguish between observation_start and realtime_start, same for end

        Parameters
        ----------
        series_id: int
            the id of the series
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred
        limit: int, default 100_000
            maximum number of observations / rows 
            range [1, 100_000]
        offset: int, default 0
            n/a, 
        sort_order: str, default 'asc' 
            return rows in ascending or descending order of observation_date 
            options are 'asc' and 'desc'
        observation_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        observation_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred
        units: str, default "lin" (no data value transformation)
            see unit_info for more information
        frequency
        aggregation_method: str, default "avg"
        output_type: int default None (realtime period)
            1: real
            2: vintage date, all observations
            3: vintage date, new and revised observations only
            4: initial release only
        vintage_dates

        Returns
        -------

        Notes
        -----
        fred/series/observations
        """
        url_prefix_params = dict(
                a_url_prefix = "series/observations?series_id=",
                a_str_id = series_id)
        url_prefix = self._append_id_to_url(**url_prefix_params)
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                "&limit=": limit,
                "&offset=": offset,
                "&sort_order=": sort_order,
                "&observation_start": observation_start,
                "&observation_end": observation_end,
                "&units": units,
                "&frequency": frequency,
                "&aggregation_method": aggregation_method,
                "&output_type=": output_type,
                "&vintage_dates=": vintage_dates,
                }
        url = self._add_optional_params(url_prefix, optional_args)
        self.series_stack[series_id] = self._fetch_data(url)
        return self.series_stack[series_id]

    def get_release_for_a_series(
            self,
            series_id: str,
            realtime_start: str = None, 
            realtime_end: str = None,
            ) -> dict:
        """
        Get the release for an economic data series.

        Parameters
        ----------
        series_id: int
            the id of the series
        observation_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        observation_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred

        Returns
        -------
        dict

        Notes
        -----
        fred/series/release
        """
        url_prefix_params = dict(
                a_url_prefix = "series/release?series_id=",
                a_str_id = series_id)
        url_prefix = self._append_id_to_url(**url_prefix_params)
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                }
        url = self._add_optional_params(url_prefix, optional_args)
        self.series_stack[series_id] = self._fetch_data(url)
        return self.series_stack[series_id]

    # case senstivity 
    def search_for_a_series(
            self, 
            search_text: list,
            search_type: str = None,
            realtime_start: str = None,
            realtime_end: str = None,
            limit: int = None,
            offset: int = None,
            order_by: str = None,
            sort_order: str = None,
            filter_variable: str = None,
            filter_value:str = None,
            tag_names: list = None,
            exclude_tag_names: list = None,
            ) -> dict:
        """
        Get economic data series that match search_text.
        **** add fred url to each method for user reference

        Parameters
        ----------
        search_text: list
            list or tuple or words to match against economic data series
        search_type: str
            one of: 'full_text', 'series_id'
            *** explain with reference to fred web service
            determines the type of search to perform
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred
        limit: int, default None (FRED will use limit = 1_000)
            maximum number of results to return
            range [1, 1_000]
        offset: non-negative integer, default None (offset of 0)
        order_by: str, default "source_count"
            order results by values of the specified attribute
            can be one of "source_count", "popularity", "created", "name", "group_id"
        sort_order: str, default None (FRED will use "asc")
            sort results in ascending or descending order for attribute values specified by order_by
        filter_variable: str default None
            the attribute to filter results by
        filter_value: str default None
            the value of the filter_variable attribute to filter results by
        tag_names: list
            list of tags (str); each tag must be present in the tag of returned series
        exclude_tag_names: list, default None (don't exclude any tags)
            tags that returned series must not have

        Returns
        -------
        dict

        Notes
        -----
        fred/series/search
        https://fred.stlouisfed.org/docs/api/fred/series_search.html
        """
        fused_search_text = self._join_strings_by(search_text, '+')
        url_prefix_params = dict(
                a_url_prefix = "series/search?search_text=",
                a_str_id = fused_search_text,
                )
        url_prefix = self._append_id_to_url(**url_prefix_params)
        optional_args = {
                "&search_type=": search_type,
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                "&limit=": limit,
                "&offset=": offset,
                "&order_by=": order_by,
                "&sort_order=": sort_order,
                "&filter_variable=": filter_variable,
                "&filter_value=": filter_value,
                "&tag_names=": tag_names,
                "&exclude_tag_names=": exclude_tag_names,
                }
        url = self._add_optional_params(url_prefix, optional_args)
        self.series_stack[fused_search_text] = self._fetch_data(url)
        return self.series_stack[fused_search_text]

    def get_tags_for_a_series_search(
            self, 
            series_search_text: list,
            realtime_start: str = None,
            realtime_end: str = None,
            tag_names: list = None,
            tag_group_id: str = None,
            tag_search_text: list = None,
            limit: int = None,
            offset: int = None,
            order_by: str = None,
            sort_order: str = None,
            ) -> dict:
        """
        Get the FRED tags for a series search. 

        Parameters
        ----------
        series_search_text: list
            list or tuple or words to match against economic data series
        search_type: str
            one of: 'full_text', 'series_id'
            *** explain with reference to fred web service
            determines the type of search to perform
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred
        tag_names: list
            list of tags (str); each tag must be present in the tag of returned series
        tag_group_id: str, default None
            a tag group id to filter tags by type with
            can be one of 'freq' for frequency, 'gen' for general or concept, 
            'geo' for geography, 'geot' for geography type, 'rls' for release, 
            'seas' for seasonal adjustment, 'src' for source
        tag_search_text: list, default None (no filtering by tag group)
            the words to find matching tags with
        limit: int, default None (FRED will use limit = 1_000)
            maximum number of results to return
            range [1, 1_000]
        offset: non-negative integer, default None (offset of 0)
        order_by: str, default "source_count"
            order results by values of the specified attribute
            can be one of "source_count", "popularity", "created", "name", "group_id"
        sort_order: str, default None (FRED will use "asc")
            sort results in ascending or descending order for attribute values specified by order_by

        Returns
        -------
        dict

        Notes
        -----
        fred/series/search/tags
        """
        search_text = self._join_strings_by(series_search_text, '+')
        url_prefix_params = dict(
                a_url_prefix = "series/search/tags?series_search_text=",
                a_str_id = search_text,
                )
        url_prefix = self._append_id_to_url(**url_prefix_params)
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                "&tag_names=": tag_names,
                "&tag_group_id=": tag_group_id,
                "&tag_search_text=": tag_search_text,
                "&limit=": limit,
                "&offset=": offset,
                "&order_by=": order_by,
                "&sort_order=": sort_order,
                }
        url = self._add_optional_params(url_prefix, optional_args)
        self.series_stack[search_text] = self._fetch_data(url)
        return self.series_stack[search_text]

    def get_related_tags_for_a_series_search(
            self, 
            series_search_text: list,
            realtime_start: str = None,
            realtime_end: str = None,
            tag_names: list = None,
            exclude_tag_names: list = None,
            tag_group_id: str = None,
            tag_search_text: list = None,
            limit: int = None,
            offset: int = None,
            order_by: str = None,
            sort_order: str = None,
            ) -> dict:
        """
        Get the related FRED tags for a series search. 

        Parameters
        ----------
        series_search_text: list
            list or tuple or words to match against economic data series
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred
        tag_names: list
            list of tags (str); each tag must be present in the tag of returned series
        exclude_tag_names: list, default None (don't exclude any tags)
            tags that returned series must not have
        tag_group_id: str, default None
            a tag group id to filter tags by type with
            can be one of 'freq' for frequency, 'gen' for general or concept, 
            'geo' for geography, 'geot' for geography type, 'rls' for release, 
            'seas' for seasonal adjustment, 'src' for source
        tag_search_text: list, default None (no filtering by tag group)
            the words to find matching tags with
        limit: int, default None (FRED will use limit = 1_000)
            maximum number of results to return
            range [1, 1_000]
        offset: non-negative integer, default None (offset of 0)
        order_by: str, default "source_count"
            order results by values of the specified attribute
            can be one of "source_count", "popularity", "created", "name", "group_id"
        sort_order: str, default None (FRED will use "asc")
            sort results in ascending or descending order for attribute values specified by order_by

        Returns
        -------
        dict

        Notes
        -----
        fred/series/search/related_tags
        """
        search_text = self._join_strings_by(series_search_text, '+')
        fused_tag_names = self._join_strings_by(tag_names, ';')
        url_prefix_params = dict(
                a_url_prefix = "series/search/related_tags?series_search_text=",
                a_str_id = search_text,
                )
        url_prefix = self._append_id_to_url(**url_prefix_params)
        url_prefix = self._append_id_to_url(url_prefix, tag_names)
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                "&tag_names=": fused_tag_names,
                "&tag_group_id=": tag_group_id,
                "&tag_search_text=": tag_search_text,
                "&limit=": limit,
                "&offset=": offset,
                "&order_by=": order_by,
                "&sort_order=": sort_order,
                }
        url = self._add_optional_params(url_prefix, optional_args)
        self.series_stack[search_text] = self._fetch_data(url)
        return self.series_stack[search_text]

    def get_tags_for_a_series(
            self,
            series_id: str,
            realtime_start: str = None,
            realtime_end: str = None,
            order_by: str = None,
            sort_order: str = None,
            ) -> dict:
        """
        Get the FRED tags for a series.

        Parameters
        ----------
        series_id: int
            the id of the series
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred
        order_by: str, default "source_count"
            order results by values of the specified attribute
            can be one of "source_count", "popularity", "created", "name", "group_id"
        sort_order: str, default None (FRED will use "asc")
            sort results in ascending or descending order for attribute values specified by order_by

        Returns
        -------
        dict

        Notes
        -----
        fred/series/tags
        """
        url_prefix_params = dict(
                a_url_prefix = "series/tags?series_id=",
                a_str_id = series_id)
        url_prefix = self._append_id_to_url(**url_prefix_params)
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                "&order_by=": order_by,
                "&sort_order=": sort_order,
                }
        url = self._add_optional_params(url_prefix, optional_args)
        self.series_stack[series_id] = self._fetch_data(url)
        return self.series_stack[series_id]

    def get_series_by_update(
            self,
            realtime_start: str = None,
            realtime_end: str = None,
            limit: int = None,
            offset: int = None,
            filter_value: str = None,
            start_time: str = None,
            end_time: str = None,
            ):
        """
        Get economic data series sorted by when observations were updated on the FRED server. 
        Results are limited to series updated within the last two weeks.

        fred/series/updates

        Parameters
        ----------
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred
        limit: int, default None (FRED will use limit = 1_000)
            maximum number of results to return
            range [1, 1_000]
        offset: non-negative integer, default None (offset of 0)
        filter_value: str default None
        start_time: str, default None
            lower bound for a time range
            can be precise to the minute
        end_time: str, default None
            upper bound for a time range
            can be precise to the minute

        Returns
        -------
        dict

        Notes
        -----
        """
        url_prefix = "series/updates?"
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                "&limit=": limit,
                "&offset=": offset,
                "&filter_value=": filter_value,
                "&start_time=": start_time,
                "&end_time=": end_time,
                }
        url = self._add_optional_params(url_prefix, optional_args)

        # change key used here to something more detailed for clarity
        self.series_stack['updates'] = self._fetch_data(url) 
        return self.series_stack['updates']

    def get_series_vintage_dates(
            self,
            series_id: str,
            realtime_start: str = None,
            realtime_end: str = None,
            limit: int = None,
            offset: int = None,
            sort_order: str = None,
            ) -> dict:
        """
        Get the dates in history when a series' data values were revised or new data values were released.
        Vintage dates are the release dates for a series excluding release dates when the 
        data for the series did not change.

        Parameters
        ----------
        series_id: int
            the id of the series
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred
        limit: int, default None (FRED will use limit = 1_000)
            maximum number of results to return
            range [1, 1_000]
        offset: non-negative integer, default None (offset of 0)
        sort_order: str, default None (FRED will use "asc")
            sort results in ascending or descending order for attribute values specified by order_by

        Returns
        -------
        dict

        Notes
        -----
        fred/series/vintagedates
        """
        url_prefix_params = dict(
                a_url_prefix = "series/vintagedates?series_id=",
                a_str_id = series_id)
        url_prefix = self._append_id_to_url(**url_prefix_params)
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                "&limit=": limit,
                "&offset=": offset,
                "&sort_order=": sort_order,
                }
        url = self._add_optional_params(url_prefix, optional_args)
        self.series_stack[series_id] = self._fetch_data(url)
        return self.series_stack[series_id]

    # fred/sources          make into class

    def get_all_sources(
            self,
            realtime_start: str = None,
            realtime_end: str = None,
            limit: int = None,
            offset: int = None,
            order_by: str = None,
            sort_order: str = None,
            ) -> dict:
        """
        Get all sources of economic data.

        Parameters
        ----------
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred
        limit: int, default None (FRED will use limit = 1_000)
            maximum number of results to return
            range [1, 1_000]
        offset: non-negative integer, default None (offset of 0)
        order_by: str, default "source_count"
            order results by values of the specified attribute
            can be one of "source_count", "popularity", "created", "name", "group_id"
        sort_order: str, default None (FRED will use "asc")
            sort results in ascending or descending order for attribute values specified by order_by

        Returns
        -------
        dict

        Notes
        -----
        fred/sources
        """
        url_prefix = "sources?"
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                "&limit=": limit,
                "&offset=": offset,
                "&order_by=": order_by,
                "&sort_order=": sort_order,
                }
        url = self._add_optional_params(url_prefix, optional_args)
        self.series_stack["sources"] = self._fetch_data(url) # improve this key
        return self.series_stack["sources"]

    def get_a_source(
            self,
            source_id: int,
            realtime_start: str = None,
            realtime_end: str = None,
            ):
        """
        Get a source of economic data.

        Parameters
        ----------
        source_id: int
            the id of the series
        realtime_start: str, default "1776-07-04" (earliest)
            YYY-MM-DD as per fred
        realtime_end: str, default "9999-12-31" (last available) 
            YYY-MM-DD as per fred

        Returns
        -------

        Notes
        -----
        fred/source
        """
        url_prefix = "source?source_id="
        try:
            url_prefix += str(source_id)
        except TypeError:
            print("Unable to cast source_id %s to str" % source_id)
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
            }
        url = self._add_optional_params(url_prefix, optional_args)
        self.source_stack[source_id] = self._fetch_data(url)
        return self.source_stack[source_id]

    def get_releases_for_a_source(
            self,
            source_id: int,
            realtime_start: str = None,
            realtime_end: str = None,
            limit: int = None,
            offset: int = None,
            order_by: str = None,
            sort_order: str = None,
            ):
        """
        Get the releases for a source.

        Parameters
        ----------
        source_id: int
            the id of the series

        realtime_start: str default None

        realtime_end: str default None

        limit: int, default None (FRED will use limit = 1_000)
            maximum number of results to return
            range [1, 1_000]

        offset: non-negative integer, default None (offset of 0)

        order_by: str, default "source_count"
            order results by values of the specified attribute
            can be one of "source_count", "popularity", "created", "name", "group_id"

        sort_order: str, default None (FRED will use "asc")
            sort results in ascending or descending order for attribute values specified by order_by

        Returns
        -------

        Notes
        -----
        fred/source/releases
        """
        url_prefix = "source/releases?source_id="
        try:
            url_prefix += str(source_id)
        except TypeError:
            print("Unable to cast source_id %s to str" % source_id)
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                "&limit=": limit,
                "&offset=": offset,
                "&order_by=": order_by,
                "&sort_order=": sort_order,
            }
        url = self._add_optional_params(url_prefix, optional_args)
        self.source_stack[source_id] = self._fetch_data(url)
        return self.source_stack[source_id]

    # fred/tags

    def get_tags(
            self,
            realtime_start: str = None,
            realtime_end: str = None,
            tag_names: list = None,
            tag_group_id: str = None,
            search_text: str = None,
            limit: int = None,
            offset: int = None,
            order_by: str = None,
            sort_order: str = None,
            ) -> dict:
        """
        Get FRED tags.

        Parameters
        ----------
        realtime_start: str default None
        realtime_end: str default None
        tag_names: list
            list of tags (str); each tag must be present in the tag of returned series
        tag_group_id: str, default None
            a tag group id to filter tags by type with
            can be one of 'freq' for frequency, 'gen' for general or concept, 
            'geo' for geography, 'geot' for geography type, 'rls' for release, 
            'seas' for seasonal adjustment, 'src' for source
        search_text: str, default None
            the words to find matching tags with
            if None, no filtering by search words
        limit: int, default None (FRED will use limit = 1_000)
            maximum number of results to return
            range [1, 1_000]
        offset: non-negative integer, default None (offset of 0)
        order_by: str, default "source_count"
            order results by values of the specified attribute
            can be one of "source_count", "popularity", "created", "name", "group_id"
        sort_order: str, default None (FRED will use "asc")
            sort results in ascending or descending order for attribute values specified by order_by

        Returns
        -------

        Notes
        -----
        fred/tags
        """
        url_prefix = "tags?"
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                "&tag_names=": tag_names,
                "&tag_group_id=": tag_group_id,
                "&search_text=": search_text,
                "&limit=": limit,
                "&offset=": offset,
                "&order_by=": order_by,
                "&sort_order=": sort_order,
            }
        url = self._add_optional_params(url_prefix, optional_args)
#        url = url.replace("tags?&", "tags?")
        self.tag_stack["tags"] = self._fetch_data(url) # make key better
        return self.tag_stack["tags"] 

    # clarify intersection of tags and union of tags*********
    def get_related_tags_for_a_tag(
            self,
            tag_names: list,
            realtime_start: str = None,
            realtime_end: str = None,
            exclude_tag_names: list = None,
            tag_group_id: str = None,
            search_text: str = None,
            limit: int = None,
            offset: int = None,
            order_by: str = None,
            sort_order: str = None,
            ):
        """
        Get related FRED tags for one or more FRED tags

        Parameters
        ----------
        tag_names: list
            list of tags (str); each tag must be present in the tag of returned series

        realtime_start: str default None

        realtime_end: str default None

        exclude_tag_names: list, default None (don't exclude any tags)
            tags that returned series must not have

        tag_group_id: str, default None
            a tag group id to filter tags by type with
            can be one of 'freq' for frequency, 'gen' for general or concept, 
            'geo' for geography, 'geot' for geography type, 'rls' for release, 
            'seas' for seasonal adjustment, 'src' for source

        search_text: str, default None
            the words to find matching tags with
            if None, no filtering by search words

        limit: int, default None (FRED will use limit = 1_000)
            maximum number of results to return
            range [1, 1_000]

        offset: non-negative integer, default None (offset of 0)

        order_by: str, default "series_count"
            order results by values of the specified attribute
            can be one of "series_count", "popularity", "created", "name", "group_id"

        sort_order: str, default None (FRED will use "asc")
            sort results in ascending or descending order for attribute values specified by order_by

        Returns
        -------

        Notes
        -----
        fred/related_tags
        """
        url_prefix = "related_tags?tag_names="
        try:
            url_prefix += ";".join(tag_names)
        except TypeError:
            print("tag_names must be list or tuple")
        optional_args = {
                "&realtime_start=": realtime_start,
                "&realtime_end=": realtime_end,
                "&exclude_tag_names=": exclude_tag_names,
                "&tag_group_id=": tag_group_id,
                "&search_text=": search_text,
                "&limit=": limit,
                "&offset=": offset,
                "&order_by=": order_by,
                "&sort_order=": sort_order,
            }
        url = self._add_optional_params(url_prefix, optional_args)
        key = "_".join(tag_names)
        self.tag_stack[key] = self._fetch_data(url)
        return self.tag_stack[key]

    def get_series_matching_tags(
            self, 
            tag_names: list,
            exclude_tag_names: list = None,
            realtime_start: str = None,
            realtime_end: str = None,
            limit: int = 100_000,
            offset: int = 0,
            order_by: str = "series_id",
            sort_order: str = "asc",
            ):
        """
        Get the metadata of series conditional on the series having ALL tags in tag_names 
        and exclude any tags in exclude_tag_names
        intersection of tag names, not union
        tag_names[0] AND tag_names[1] AND ... tag_names[n - 1] must be in returned series' tags
        double-check filtering mechanism (name or tag of series?)
        all fred params:
            
        Parameters
        ----------
        tag_names: list
            list of tags (str); each tag must be present in the tag of returned series

        exclude_tag_names: list, default None
            example: ['alcohol', 'quarterly',] to exclude series with either tag 'alcohol' or tag 'quarterly'

        realtime_start: str default None

        realtime_end: str default None

        limit: int, default 1_000
            maximum number of observations / rows 
            range [1, 1_000]

        Returns
        -------

        Notes
        -----
        fred/tags/series
        """
        # perhaps check first to see if there's a matching query in self.tag_stack
        url_prefix = "tags/series?tag_names=" 
        try:
            url_prefix += ";".join(tag_names)
        except TypeError:
            print("tag_names must be list or tuple")
        # make each returned series a FredSeries
        realtime_period = self._get_realtime_date(
                realtime_start, 
                realtime_end
                )
        url_prefix += realtime_period
#        breakpoint()
        key = "_".join(tag_names)
        self.tag_stack[key] = self._fetch_data(url_prefix)
        return self.tag_stack[key]


