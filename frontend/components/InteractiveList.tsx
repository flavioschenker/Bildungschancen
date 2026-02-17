interface ColumnDef<T> {
    key: keyof T;
    header: string;
    width?: string;
}

interface ComponentProps<T> {
    headers: (keyof T)[];
    rows: T[];
}

export default <T,>({headers, rows}: ComponentProps<T>) => {
    return (
        <div className="grid grid-cols-1">
            <div className="flex gap-1">
                {headers.map(header => (
                    <div>{String(header)}</div>
                ))}
            </div>
            <div>
                {rows.map(row => (
                    <div className="flex">
                        {
                            headers.map(header => (
                                <div>{String(row[header])}</div>
                            ))
                        }
                    </div>
                ))}
            </div>
        </div>
    )
}