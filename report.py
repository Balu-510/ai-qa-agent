def generate_report(results):
    return {
        "total": len(results),
        "passed": len([r for r in results if "Passed" in r]),
        "failed": len([r for r in results if "Failed" in r]),
        "details": results
    }