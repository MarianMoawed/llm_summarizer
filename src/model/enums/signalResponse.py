from enum import Enum

class SignalResponse(Enum):

    NONE_GENERATION_CLENT = "generation client was not set"
    FILE_TYPE_NOT_SUPPORTED_ERROR = "file_type_not_supported"
    FILE_UPLOADED_SUCCESSFULLY = "file_uploaded_successfully"
    FILE_SAVING_ERROR = "error_saving_file"
    FILE_ID_ERROR = "no_file_found_with_this_id"
    NO_ASSETS_FOUND_ERROR = "no_assets_found_for_this_project"
    CHUNKS_DELETED_SUCCESSFULLY = "chunks_deleted_successfully"
    CHUNKS_INSERTED_SUCCESSFULLY = "chunks_inserted_successfully"