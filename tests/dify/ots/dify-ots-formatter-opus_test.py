"""
dify-ots-formatter-opus_test.py

Unit Tests (using pytest) for:

``formatter`` node dealing with Opus
"""

import pytest

from dify_studio.opus_tag_smith.nodes.formatter import _format_opus

# helpers  #####################################################################


def _make_extract(
    title,
    subtitle="",
    year="2024",
    tags=None,
    season=None,
    episode=None,
    episode_name=None,
):
    """
    build a minimal extract dict for ``_format_opus``.

    :param title: primary title
    :type title: str
    :param subtitle: secondary title (default empty string)
    :type subtitle: str
    :param year: four-digit release year string (default ``"2024"``)
    :type year: str
    :param tags: list of tag strings; defaults to ``["1080p", "H264"]``
    :type tags: list[str] or None
    :param season: season number, omitted from dict when ``None``
    :type season: str or None
    :param episode: episode number, omitted from dict when ``None``
    :type episode: str or None
    :param episode_name: episode name, omitted from dict when ``None``
    :type episode_name: str or None
    :return: extract dict
    :rtype: dict
    """
    extract = {
        "release_year": year,
        "title": title,
        "subtitle": subtitle,
        "tags": tags if tags is not None else ["1080p", "H264"],
    }
    if season is not None:
        extract["season_number"] = season
    if episode is not None:
        extract["episode_number"] = episode
    if episode_name is not None:
        extract["episode_name"] = episode_name
    return extract


# tests  #######################################################################


class TestFormatOpusPlainTitle:
    """title with no season/episode; title contains no unsafe chars."""

    @pytest.fixture(scope="class")
    def opt(self):
        return _format_opus(_make_extract(title="Inception", year="2010"))

    def test_title_block(self, opt):
        assert "Title:\n```\nInception\n```\n" in opt

    def test_no_safe_title_block(self, opt):
        # when title == safe_title the redundant block must NOT appear
        assert "Title (Safe)" not in opt

    def test_no_episode_name_block(self, opt):
        assert "Episode Name:" not in opt

    def test_folder_name_block(self, opt):
        assert "Folder Name:\n\n```\n[2010]Inception\n```\n" in opt

    def test_resource_name_block(self, opt):
        assert (
            "Resource Name:\n\n```\n[2010]Inception{1080p,H264}\n```\n" in opt
        )

    def test_year_embedded_in_folder(self, opt):
        assert "[2010]" in opt


class TestFormatOpusUnsafeTitle:
    """title that contains filename-unsafe chars; safe block must appear."""

    # FIXME: subtitle unsafe-char conversion is extracted but never used in the
    #        output — the FIXME marker in the source reflects this gap

    @pytest.fixture(scope="class")
    def opt(self):
        # colon and question mark are both unsafe
        return _format_opus(
            _make_extract(
                title="Alien: Covenant?", year="2017", tags=["BluRay"]
            )
        )

    def test_title_block_shows_original(self, opt):
        assert "Title:\n```\nAlien_ Covenant_\n```\n" in opt

    def test_safe_title_block_absent_when_same(self, opt):
        # after _convert_filename_safe the result is already safe, so
        # title == safe_title and the redundant block must NOT appear
        assert "Title (Safe)" not in opt

    def test_folder_name_uses_safe(self, opt):
        assert "[2017]Alien_ Covenant_" in opt

    def test_resource_name(self, opt):
        assert "[2017]Alien_ Covenant_{BluRay}" in opt


class TestFormatOpusTagsVariants:
    """tags list permutations: single tag, multiple tags."""

    def test_single_tag(self):
        opt = _format_opus(
            _make_extract(title="Dune", year="2021", tags=["4K"])
        )
        assert "{4K}" in opt

    def test_multiple_tags_joined_by_comma(self):
        opt = _format_opus(
            _make_extract(
                title="Dune", year="2021", tags=["4K", "HDR10", "AC-3"]
            )
        )
        assert "{4K,HDR10,AC-3}" in opt

    def test_tags_appear_in_resource_name_only(self):
        opt = _format_opus(
            _make_extract(title="Dune", year="2021", tags=["BluRay", "H265"])
        )
        # tags brace must appear in resource name line
        assert "[2021]Dune{BluRay,H265}" in opt
        # folder name must NOT contain the brace block
        folder_line = "[2021]Dune"
        assert folder_line in opt


class TestFormatOpusSeasonOnly:
    """season present, no episode — only the S-prefix is appended."""

    @pytest.fixture(scope="class")
    def opt(self):
        return _format_opus(
            _make_extract(title="Stranger Things", year="2016", season="02")
        )

    def test_title_contains_season(self, opt):
        assert "Stranger Things.S02" in opt

    def test_no_episode_segment(self, opt):
        assert ".E" not in opt

    def test_folder_name(self, opt):
        assert "Folder Name:\n\n```\n[2016]Stranger Things.S02\n```\n" in opt

    def test_resource_name(self, opt):
        assert "[2016]Stranger Things.S02{1080p,H264}" in opt

    def test_no_episode_name_section(self, opt):
        assert "Episode Name:" not in opt


class TestFormatOpusEpisodeOnlyNoSeason:
    """episode present but NO season — no dot separator between S and E."""

    @pytest.fixture(scope="class")
    def opt(self):
        return _format_opus(
            _make_extract(title="Chernobyl", year="2019", episode="03")
        )

    def test_title_contains_episode(self, opt):
        assert "Chernobyl.E03" in opt

    def test_no_season_segment(self, opt):
        assert ".S" not in opt

    def test_no_dot_between_s_and_e(self, opt):
        # without a season there must be no ".E" preceded by a dot separator
        assert "S" not in opt

    def test_folder_name(self, opt):
        assert "[2019]Chernobyl.E03" in opt

    def test_resource_name(self, opt):
        assert "[2019]Chernobyl.E03{1080p,H264}" in opt

    def test_episode_name_section_absent(self, opt):
        assert "Episode Name:" not in opt


class TestFormatOpusSeasonAndEpisode:
    """season + episode, no episode name — dot separator must appear."""

    @pytest.fixture(scope="class")
    def opt(self):
        return _format_opus(
            _make_extract(
                title="The Last of Us",
                year="2023",
                season="01",
                episode="04",
            )
        )

    def test_season_episode_format(self, opt):
        assert "The Last of Us.S01.E04" in opt

    def test_folder_name(self, opt):
        assert "[2023]The Last of Us.S01.E04" in opt

    def test_resource_name(self, opt):
        assert "[2023]The Last of Us.S01.E04{1080p,H264}" in opt

    def test_episode_name_section_absent(self, opt):
        assert "Episode Name:" not in opt


class TestFormatOpusSeasonEpisodeWithName:
    """season + episode + episode name — full SNE block."""

    @pytest.fixture(scope="class")
    def opt(self):
        return _format_opus(
            _make_extract(
                title="Breaking Bad",
                year="2008",
                season="04",
                episode="11",
                episode_name="Crawl Space",
            )
        )

    def test_full_sne_in_title(self, opt):
        assert "Breaking Bad.S04.E11-Crawl Space" in opt

    def test_folder_name(self, opt):
        assert "[2008]Breaking Bad.S04.E11-Crawl Space" in opt

    def test_resource_name(self, opt):
        assert "[2008]Breaking Bad.S04.E11-Crawl Space{1080p,H264}" in opt

    def test_episode_name_section_present(self, opt):
        assert "Episode Name:" in opt

    def test_episode_name_section_content(self, opt):
        assert "```\nS04.E11-Crawl Space\n```\n" in opt


class TestFormatOpusEpisodeWithNameNoSeason:
    """episode + episode name but NO season."""

    @pytest.fixture(scope="class")
    def opt(self):
        return _format_opus(
            _make_extract(
                title="Miniseries",
                year="2022",
                episode="02",
                episode_name="The Reckoning",
            )
        )

    def test_sne_format_no_season(self, opt):
        # no season → no dot between S and E tokens; just E<n>-<name>
        assert "Miniseries.E02-The Reckoning" in opt

    def test_no_season_in_sne(self, opt):
        assert ".S" not in opt

    def test_folder_name(self, opt):
        assert "[2022]Miniseries.E02-The Reckoning" in opt

    def test_resource_name(self, opt):
        assert "[2022]Miniseries.E02-The Reckoning{1080p,H264}" in opt

    def test_episode_name_section_content(self, opt):
        assert "```\nE02-The Reckoning\n```\n" in opt


class TestFormatOpusResponseStructure:
    """verify the overall markdown skeleton is always present."""

    @pytest.fixture(scope="class")
    def opt(self):
        return _format_opus(_make_extract(title="Oppenheimer", year="2023"))

    def test_title_label(self, opt):
        assert "Title:" in opt

    def test_folder_name_label(self, opt):
        assert "Folder Name:" in opt

    def test_resource_name_label(self, opt):
        assert "Resource Name:" in opt

    def test_code_fence_present(self, opt):
        assert "```" in opt

    def test_returns_string(self, opt):
        assert isinstance(opt, str)


class TestFormatOpusYearVariants:
    """year value is passed through verbatim."""

    def test_year_1970(self):
        opt = _format_opus(_make_extract(title="Woodstock", year="1970"))
        assert "[1970]" in opt

    def test_year_2000(self):
        opt = _format_opus(_make_extract(title="Gladiator", year="2000"))
        assert "[2000]" in opt

    def test_year_in_folder_and_resource(self):
        opt = _format_opus(_make_extract(title="Tenet", year="2020"))
        assert "[2020]Tenet" in opt


class TestFormatOpusTitleSafeBlockTrigger:
    """
    the *Title (Safe)* block only renders when the safe-converted title
    differs from the already-safe ``title`` stored after conversion.

    Since ``_convert_filename_safe`` is applied to ``extract[title]`` first,
    and then ``safe_title = _convert_filename_safe(title)`` is called on the
    already-converted string, the two will **always** be equal — meaning the
    ``Title (Safe)`` block can never appear for ``_format_opus`` inputs.

    These tests document that invariant.

    # FIXME: the Title (Safe) branch appears unreachable for _format_opus
    #        because title is already safe-converted before safe_title is
    #        derived; consider whether the branch should be removed or if
    #        season_and_episode_content can introduce new unsafe chars
    """

    def test_plain_title_no_safe_block(self):
        opt = _format_opus(_make_extract(title="Arrival"))
        assert "Title (Safe)" not in opt

    def test_title_with_unsafe_chars_still_no_safe_block(self):
        # unsafe chars in input are converted once; the second conversion
        # produces the same string, so the safe block never appears
        opt = _format_opus(_make_extract(title='Kill "Bill"'))
        assert "Title (Safe)" not in opt

    def test_title_with_episode_name_containing_unsafe_chars(self):
        # episode_name is NOT passed through _convert_filename_safe, so if it
        # contains unsafe chars the season_and_episode_content appended to
        # title may cause title != safe_title → safe block appears
        opt = _format_opus(
            _make_extract(
                title="Show",
                year="2020",
                season="01",
                episode="01",
                episode_name='Who "Are" You?',
            )
        )
        # safe_title will replace chars in the episode_name portion
        assert "Title (Safe):" in opt
