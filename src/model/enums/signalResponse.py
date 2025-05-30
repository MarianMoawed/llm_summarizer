from enum import Enum

class SignalResponse(Enum):

    NONE_GENERATION_CLENT = "generation client was not set"
    FILE_TYPE_NOT_SUPPORTED_ERROR = "file_type_not_supported"
    FILE_UPLOADED_SUCCESSFULLY = "file_uploaded_successfully"
    FILE_SAVING_ERROR = "error_saving_file"