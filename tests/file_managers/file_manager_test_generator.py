import string
import hypothesis.strategies as st
from hypothesis import strategies as st


@st.composite
def valid_directory_names(draw):
    valid_chars = string.ascii_letters + string.digits + '-_'
    length = draw(st.integers(min_value=1, max_value=20))
    return draw(st.text(alphabet=valid_chars, min_size=length, max_size=length))


@st.composite
def invalid_directory_names(draw):
    invalid_chars = ''.join(set(string.punctuation) - set('-_'))
    length = draw(st.integers(min_value=1, max_value=20))
    return draw(st.text(alphabet=invalid_chars, min_size=length, max_size=length))


@st.composite
def valid_file_names(draw):
    valid_chars = string.ascii_letters + string.digits + '-_'
    base_name = draw(
        st.text(alphabet=valid_chars, min_size=1, max_size=20))

    extension = draw(st.text(alphabet=valid_chars, min_size=1, max_size=5))
    has_extension = draw(st.booleans())

    if has_extension:
        file_name = f"{base_name}.{extension}"
    else:
        file_name = base_name

    return file_name


@st.composite
def invalid_file_names(draw):
    invalid_chars = ''.join(set(string.punctuation) - set('-_.'))
    length = draw(st.integers(min_value=1, max_value=20))
    return draw(st.text(alphabet=invalid_chars, min_size=length, max_size=length))
