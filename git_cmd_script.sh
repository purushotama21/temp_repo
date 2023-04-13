if ! git_status_output="$(git status --porcelain)"; then
    # `git status` had an error
    error_code="$?"
    echo "'git status' had an error: $error_code" 
    # exit 1  # (optional)
elif [ -z "$git_status_output" ]; then
    # Working directory is clean
    echo "Working directory is clean."
else
    # Working directory has uncommitted changes.
    echo "Working directory has UNCOMMITTED CHANGES."
    git add .
    git commit -m "data share name replaced @Build_Number ${BUILD_NUMBER}"
    # git push origin master
    # exit 2  # (optional)
fi