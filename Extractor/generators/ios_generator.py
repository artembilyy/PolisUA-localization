import os
import stat
import json

def generate_ios(all_tables, output_dir, enum_output):
    # Sort categories for consistent output
    sorted_categories = sorted(all_tables.keys())
    
    # Initialize Swift enum content for RSKey.swift
    swift_enum_content = """\
//
//  RSKey.swift
//  Copyright © PolisUA
//  All rights reserved.
//
// WARNING: This file is auto-generated and locked for editing. Do not modify manually!
//

public enum RSKey {
"""
    # Generate enum cases for each category
    for category in sorted_categories:
        swift_enum_content += f"    case {category.lower()}({category})\n"

    # Add factory registration and initialization logic
    swift_enum_content += """
    // MARK: - Factory Registration
    private typealias KeyFactory = (String) -> RSKey?
    private static var keyFactories: [String: KeyFactory] = [:]

    public static func registerFactory(_ factory: any LocalizableKey.Type) {
        keyFactories[factory.tableName.lowercased()] = factory.makeKey
    }

    // MARK: - Initialization
    public init?(rawValue: String) {
        let parts = rawValue.split(separator: ".", maxSplits: 1)
        guard parts.count == 2 else { return nil }

        let tableName = String(parts[0]).lowercased()
        let keyValue = String(parts[1])

        guard let factory = Self.keyFactories[tableName] else { return nil }
        guard let key = factory(keyValue) else { return nil }
        self = key
    }

    // MARK: - Wrapped Value
    public func wrappedValue() -> any LocalizableKey {
        switch self {
"""
    # Generate switch cases for wrapped values
    for category in sorted_categories:
        swift_enum_content += f"        case .{category.lower()}(let wrappedValue):\n            return wrappedValue\n"

    swift_enum_content += "        }\n    }\n\n"

    # Generate sub-enums for each category
    for category in sorted_categories:
        swift_enum_content += f"    // MARK: - {category}.xstrings\n"
        swift_enum_content += f"    public enum {category}: String, LocalizableKey {{\n"
        sorted_keys = sorted(all_tables[category].keys())
        for key in sorted_keys:
            swift_enum_content += f"        case {key}\n"
        swift_enum_content += f"""
        public var tableName: String {{
            Self.tableName
        }}

        public static var keyMapper: (Self) -> RSKey {{
            {{ key in .{category.lower()}(key) }}
        }}

        public static let _register: Void = {{
            RSKey.registerFactory({category}.self)
            return ()
        }}()
"""
        swift_enum_content += "    }\n\n"

    # Finalize Swift enum content
    swift_enum_content = swift_enum_content.rstrip() + "\n}\n"

    # Create output directory if it doesn't exist
    os.makedirs(output_dir, exist_ok=True)
    # Ensure the output file is writable if it exists
    if os.path.exists(enum_output):
        os.chmod(enum_output, stat.S_IRUSR | stat.S_IWUSR | stat.S_IRGRP | stat.S_IROTH)
    
    # Write RSKey.swift file
    with open(enum_output, 'w', encoding='utf-8') as f:
        f.write(swift_enum_content)
    
    # Lock the file to read-only
    os.chmod(enum_output, stat.S_IRUSR | stat.S_IRGRP | stat.S_IROTH)
    print(f"Generated {enum_output} and locked for editing")

    # Generate .xcstrings files for each category
    for category in sorted_categories:
        xcstrings_data = {
            "sourceLanguage": "en",
            "version": "1.0",
            "strings": {}
        }
        sorted_keys = sorted(all_tables[category].keys())
        for key in sorted_keys:
            xcstrings_data["strings"][key] = {
                "localizations": {
                    lang: {
                        "stringUnit": {
                            "state": "translated",
                            "value": value
                        }
                    } for lang, value in all_tables[category][key].items()
                }
            }

        # Write .xcstrings file
        category_output = os.path.join(output_dir, f"{category}.xcstrings")
        with open(category_output, 'w', encoding='utf-8') as f:
            json.dump(xcstrings_data, f, ensure_ascii=False, indent=2)
        print(f"Generated {os.path.basename(category_output)}")
