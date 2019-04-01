import { IResource } from 'src/app/editor/shared/models/resource.model';

const ICONS_MAP = {
    'js': 'fab fa-js-square',
    'py': 'fab fa-python',
    'pdf': 'fas fa-file-pdf',
    'css': 'fab fa-css3',
    'less': 'fab fa-css3',
    'scss': 'fab fa-css3',
    'html': 'fab fa-html5',
    'csv': 'fas fa-file-csv',
    'xls': 'fas fa-file-pdf',
    'java': 'fab fa-java',
    'png': 'fas fa-file-image',
    'jpg': 'fas fa-file-image',
    'svg': 'fas fa-file-image',
};

/**
 * Returns the last portion of a path. Similar to the Unix basename command.
 * Often used to extract the file name from a fully qualified path.
 * @param the path to evaluate.
 */
export function basename(path: string) {
    if (!path) {
        return path;
    }
    path = path.replace(/\\/g, '/');
    return path.slice(path.lastIndexOf('/') + 1, path.length);
}

/**
 * Returns the directory name of a path. Similar to the Unix dirname command.
 * @param path the path to evaluate
 */
export function dirname(path: string) {
    if (!path) {
        return path;
    }
    path = path.replace(/\\/g, '/');
    let head = path.slice(0, path.lastIndexOf('/') + 1);
    if (head && !head.match(/^\/*$/g)) {
      head = head.replace(/\/*$/g, '');
    }
    return head;
}

/**
 * Returns the extension of the path (in lowercase), from the last '.' to end of string in the last portion of the path.
 * If there is no '.' in the last portion of the path or the first character of it is '.', then it returns an empty string
 * @param path the path to evaluate
 */
export function extname(path: string) {
    const base = basename(path);
    if (!base) {
        return base;
    }
    if (base.startsWith('.')) {
        return '';
    }
    const dotIndex = base.lastIndexOf('.');
    if (dotIndex === -1) {
        return '';
    }
    return base.substring(dotIndex + 1).toLowerCase();
}

/**
 * Finds the font awesome icon representing the most the given path.
 * If an icon is not found, fallback will be returned.
 * @param path the path to evaluate
 * @param fallback the icon to return if the function cannot find an icon.
 */
export function findIcon(path: string, fallback: string) {
    const ext = extname(path);
    if (ext in ICONS_MAP) {
        return ICONS_MAP[ext];
    }
    return fallback;
}
